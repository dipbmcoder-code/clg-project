let beforeupdateData;
'use strict';
/* global strapi */

const axios = require('axios');
const crypto = require("crypto");
const {decode} = require('entities');

function getEncryptionKey() {
    const keyBase64 = process.env.PASSWORD_SECRET_KEY;
    
    if (!keyBase64) {
        throw new Error('PASSWORD_SECRET_KEY not set');
    }
    
    // Convert URL-safe base64 to standard base64
    let standardBase64 = keyBase64
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    
    // Add padding
    const padCount = (4 - (standardBase64.length % 4)) % 4;
    standardBase64 += '='.repeat(padCount);
    
    const keyBuffer = Buffer.from(standardBase64, 'base64');
    
    if (keyBuffer.length !== 32) {
        throw new Error(`Key must decode to 32 bytes, got ${keyBuffer.length}`);
    }
    
    return keyBuffer;
}

const fs = require('fs');
const path = require('path');

const ENC_KEY = getEncryptionKey();
 
function encryptPassword(text) {
    const cipher = crypto.createCipheriv('aes-256-ecb', ENC_KEY, null);
    let encrypted = cipher.update(text, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
}
function decryptPassword(encrypted) {
    try {
        const decipher = crypto.createDecipheriv('aes-256-ecb', ENC_KEY, null);
        let decrypted = decipher.update(encrypted, 'base64', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    } catch (error) {
        console.error('Decryption error:', error);
        return encrypted;
    }
}

// Function to validate WordPress credentials
async function validateWordPressCredentials(username, password, siteUrl) {
    const auth = Buffer.from(`${username}:${password}`).toString("base64");
    try {
        // Call the WP REST API with Basic Auth
        const response = await axios({
            method: 'get',
            url: `${siteUrl}/wp-json/wp/v2/users/me`,
            headers: {
                'Authorization': `Basic ${auth}`
            }
        });
        return response.status === 200;
    } catch (error) {
        console.error("Error validating user:", error);
        return false;
    }
}

async function fetchWordpressCategories(username, password, siteUrl, page=1) {
    const auth = Buffer.from(`${username}:${password}`).toString("base64");

    try {
        // Call the WP REST API with Basic Auth
        const response = await axios({
            method: 'get',
            url: `${siteUrl}/wp-json/wp/v2/categories?per_page=100&page=${page}`,
            headers: {
                'Authorization': `Basic ${auth}`
            }
        });
        if (response.status === 200) {
            return response.data; // Return categories data
        } else {
            throw new Error(`Failed to fetch categories, status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
        throw error;
    }
}

async function fetchWordpressAuthors(username, password, siteUrl, page=1) {
    const auth = Buffer.from(`${username}:${password}`).toString("base64");

    try {
        // Call the WP REST API with Basic Auth
        const response = await axios({
            method: 'get',
            url: `${siteUrl}/wp-json/wp/v2/users?roles=author,editor,administrator&per_page=100&page=${page}`,
            headers: {
                'Authorization': `Basic ${auth}`
            }
        });
        if (response.status === 200) {
            return response.data; // Return authors data
        } else {
            throw new Error(`Failed to fetch authors, status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching authors:", error);
        throw error;
    }
}

let beforeUpdatePassword = "";

module.exports = {
    // After fetching a single website entry
    async afterFindOne (result, params) {
        if (!result) return result;

        if (result?.result?.platform_user && result?.result?.platform_password && result?.result?.platform_url) {
            try {
                const decryptedPassword = decryptPassword(result.result.platform_password) || result.result.platform_password;
                beforeUpdatePassword = decryptedPassword;
                if (decryptedPassword === null) {
                    throw new Error("Failed to decrypt password");
                }
                if (!result?.result?.is_validated) {
                    result.result.categoriesOptions = [];
                    return result;
                }
                if (result.result.platform_url) {
                    result.result.platform_url = result.result.platform_url.trim().replace(/\/+$/, '').replace(/^(https?:\/\/)www\./, '$1'); // remove trailing slashes and "www." after http:// or https://
                }
                let categories = await fetchWordpressCategories(result.result.platform_user, decryptedPassword, result.result.platform_url);
                if (categories.length === 100) {
                    const moreCategories = await fetchWordpressCategories(result.result.platform_user, decryptedPassword, result.result.platform_url, 2);
                    categories = categories.concat(moreCategories);
                }
                result.result.categoriesOptions = categories.map(cat => ({ id: cat.id, name: decode(cat.name) })) || [];

                let authors = await fetchWordpressAuthors(result.result.platform_user, decryptedPassword, result.result.platform_url);
                if (authors.length === 100) {
                    const moreAuthors = await fetchWordpressAuthors(result.result.platform_user, decryptedPassword, result.result.platform_url, 2);
                    authors = authors.concat(moreAuthors);
                }
                result.result.authorsOptions = authors.map(auth => ({ id: auth.id, name: decode(auth.name) })) || [];
            } catch (error) {
                console.error("Failed to fetch WordPress categories or Authors:", error);
                result.result.categoriesOptions = [];
                result.result.authorsOptions = [];
            }
        } else {
            if (result?.result) {
                result.result.categoriesOptions = [];
                result.result.authorsOptions = [];
            }
        }
        return result;
    },

    async beforeCreate(event) {
        const { params } = event;
        let platform_password = null;
        if (params?.data?.platform_url) {
            params.data.platform_url = params.data.platform_url.trim().replace(/\/+$/, '').replace(/^(https?:\/\/)www\./, '$1'); // remove trailing slashes and "www." after http:// or https://
        }
        // Validate WordPress credentials
        if (params?.data?.platform_user && params?.data?.platform_password) {
            platform_password = decryptPassword(params.data.platform_password);
            const isValid = await validateWordPressCredentials(params.data.platform_user, platform_password, params.data.platform_url);
            params.data.is_validated = !!isValid;
        }
        if (platform_password && beforeUpdatePassword != platform_password) {
            params.data.platform_password = encryptPassword(platform_password);
        }
    },

    async beforeUpdate(event) {
        const { params, data } = event; 
        let platform_password = null;
        if (params?.data?.platform_url) {
            params.data.platform_url = params.data.platform_url.trim().replace(/\/+$/, '').replace(/^(https?:\/\/)www\./, '$1'); // remove trailing slashes and "www." after http:// or https://
        }
        if (params?.data?.platform_user || params?.data?.platform_password || params?.data?.platform_url) {
            // Fetch existing record to get current values if not provided in update
            const existing = await strapi.entityService.findOne('api::users-website.users-website', params?.where?.id);

            params.data.platform_user = params?.data?.platform_user || existing.platform_user;
            platform_password = params?.data?.platform_password || existing.platform_password;
            platform_password = decryptPassword(platform_password);
            params.data.platform_url = params?.data?.platform_url || existing.platform_url;

            const isValid = await validateWordPressCredentials(params.data.platform_user, platform_password, params.data.platform_url);
            params.data.is_validated = !!isValid;
        }
        if (platform_password && beforeUpdatePassword != platform_password) {
            params.data.platform_password = encryptPassword(platform_password);
        }
    },

}