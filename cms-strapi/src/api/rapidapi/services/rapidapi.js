'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');

module.exports = ({ strapi }) => ({
  async fetchLeagues() {
    try {
      const filePath = path.join(process.cwd(), 'public', 'uploads', 'leagues.json');
      if (!fs.existsSync(filePath)) {
        return { leagues: [] };
      }
      const rawData = fs.readFileSync(filePath, 'utf8');
      const data = JSON.parse(rawData);
      if (data?.response) {
        data.response = data.response.map(res=>({id:res.league.id,name:res.league.name, country: res.country.name})) || [];
      }
      return {leagues: data?.response || []};
    } catch (error) {
      strapi.log.error('Error reading leagues data:', error);
      return { leagues: [] };
    }
  },

  async fetchPlayers(search) {
    try {
      console.log("search",search)
      const season = new Date().getFullYear();
      const searchText = search || '';
      const url = `${process.env.RAPID_API_URL}/players/profiles${searchText ? `?search=${searchText}` : ''}`
      console.log("url",url)
      const response = await axios.get(url, {
        headers: {
          'X-RapidAPI-Key': process.env.RAPID_API_KEY,
          'X-RapidAPI-Host': process.env.RAPID_API_HOST,
        },
      });
      if (response.data?.response) {
        response.data.response = response.data.response.map(res=>({id:res.player.id,name:res.player.name, position: res.player.position})) || [];
      }
      return { players: response.data?.response || [] };
    } catch (error) {
      strapi.log.error('Error reading players data:', error);
      return { players: [] };
    }
  },
});
