"use strict";
/* global strapi */

module.exports = {
  async fetchPlayers(ctx) {
    try {
      const { leagueId } = ctx.params;
      const { search } = ctx.query;
      const data = await strapi.service('api::rapidapi.rapidapi').fetchPlayers(search);
      ctx.body = data;
    } catch (error) {
      ctx.throw(500, error.response?.data || "Error fetching players");
    }
  },
  async fetchLeagues(ctx) {
    try {
      const data = await strapi.service('api::rapidapi.rapidapi').fetchLeagues();
      ctx.body = data;
    } catch (error) {
      ctx.throw(500, error.response?.data || "Error fetching leagues");
    }
  },
};
