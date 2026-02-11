'use strict';

/**
 * websites-news service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::websites-news.websites-news');
