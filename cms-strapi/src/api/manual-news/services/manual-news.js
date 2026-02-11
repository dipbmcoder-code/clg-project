'use strict';

/**
 * manual-news service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::manual-news.manual-news');
