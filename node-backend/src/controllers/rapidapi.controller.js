const fetch = require('node-fetch');
const prisma = require('../config/database');
const logger = require('../config/logger');

const getLeagues = async (req, res, next) => {
  try {
    const settings = await prisma.aiSettings.findFirst();
    if (!settings?.rapidapiKey) {
      return res.status(400).json({ error: { message: 'RapidAPI key not configured' } });
    }

    const response = await fetch('https://v3.football.api-sports.io/leagues', {
      headers: {
        'x-rapidapi-key': settings.rapidapiKey,
        'x-rapidapi-host': 'v3.football.api-sports.io',
      },
    });

    const data = await response.json();
    res.json({ data: data.response || [] });
  } catch (err) {
    logger.error(`RapidAPI leagues error: ${err.message}`);
    next(err);
  }
};

const getPlayerProfiles = async (req, res, next) => {
  try {
    const { search } = req.query;
    if (!search) {
      return res.status(400).json({ error: { message: 'Search query required' } });
    }

    const settings = await prisma.aiSettings.findFirst();
    if (!settings?.rapidapiKey) {
      return res.status(400).json({ error: { message: 'RapidAPI key not configured' } });
    }

    const response = await fetch(
      `https://v3.football.api-sports.io/players?search=${encodeURIComponent(search)}&season=${req.query.season || new Date().getFullYear()}`,
      {
        headers: {
          'x-rapidapi-key': settings.rapidapiKey,
          'x-rapidapi-host': 'v3.football.api-sports.io',
        },
      }
    );

    const data = await response.json();
    res.json({ data: data.response || [] });
  } catch (err) {
    logger.error(`RapidAPI players error: ${err.message}`);
    next(err);
  }
};

module.exports = { getLeagues, getPlayerProfiles };
