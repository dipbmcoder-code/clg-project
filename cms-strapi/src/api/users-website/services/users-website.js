'use strict';

/**
 * users-website service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::users-website.users-website');
