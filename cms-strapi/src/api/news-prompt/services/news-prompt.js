'use strict';

/**
 * news-prompt service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::news-prompt.news-prompt');
