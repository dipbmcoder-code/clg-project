'use strict';

/**
 * manual-news controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

// module.exports = createCoreController('api::manual-news.manual-news');
module.exports = createCoreController('api::manual-news.manual-news', ({ strapi }) => ({
  async find(ctx) {
    const entries = await strapi.entityService.findMany('api::manual-news.manual-news', {
      populate: {
        users_websites: true,  // ✅ full websites objects
        websites_news: {
          populate: '*',  // ✅ nested relation inside websites_news
        },
      },
    });

    return entries;
  },

  // async findOne(ctx) {
  //   const { id } = ctx.params;

  //   const entry = await strapi.entityService.findOne('api::manual-news.manual-news', id, {
  //     populate: '*',
  //   });

  //   return entry;
  // },
}));