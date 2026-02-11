'use strict';

/**
 * news-log service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::news-log.news-log');
