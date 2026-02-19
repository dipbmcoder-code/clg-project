const prisma = require('../config/database');
const logger = require('../config/logger');

// Mask sensitive keys for display
const maskKey = (key) => {
  if (!key) return null;
  if (key.length <= 8) return '••••••••';
  return key.substring(0, 4) + '••••••••' + key.substring(key.length - 4);
};

const get = async (req, res, next) => {
  try {
    let settings = await prisma.aiSettings.findFirst();
    if (!settings) {
      settings = await prisma.aiSettings.create({ data: {} });
    }

    // Return masked version
    const masked = {
      ...settings,
      openaiApiKey: maskKey(settings.openaiApiKey),
      openrouterApiKey: maskKey(settings.openrouterApiKey),
      geminiApiKey: maskKey(settings.geminiApiKey),
      rapidapiKey: maskKey(settings.rapidapiKey),
      awsAccessKey: maskKey(settings.awsAccessKey),
      awsSecretKey: maskKey(settings.awsSecretKey),
      sendgridApiKey: maskKey(settings.sendgridApiKey),
      // Include a flag indicating if keys are set
      _hasOpenaiKey: !!settings.openaiApiKey,
      _hasOpenrouterKey: !!settings.openrouterApiKey,
      _hasGeminiKey: !!settings.geminiApiKey,
      _hasRapidapiKey: !!settings.rapidapiKey,
      _hasAwsKeys: !!(settings.awsAccessKey && settings.awsSecretKey),
      _hasSendgridKey: !!settings.sendgridApiKey,
    };

    res.json({ data: masked });
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    const data = { ...req.body };
    // Strip fields that shouldn't be updated directly
    delete data.id;
    delete data.createdAt;
    delete data.updatedAt;

    // Don't overwrite keys with masked values
    const maskedFields = [
      'openaiApiKey', 'openrouterApiKey', 'geminiApiKey',
      'rapidapiKey', 'awsAccessKey', 'awsSecretKey', 'sendgridApiKey',
    ];

    maskedFields.forEach((field) => {
      if (data[field] && data[field].includes('••••')) {
        delete data[field];
      }
    });

    let settings = await prisma.aiSettings.findFirst();
    if (!settings) {
      settings = await prisma.aiSettings.create({ data });
    } else {
      settings = await prisma.aiSettings.update({
        where: { id: settings.id },
        data,
      });
    }

    logger.info(`AI settings updated by ${req.user.email}`);
    res.json({ data: { message: 'Settings updated successfully' } });
  } catch (err) {
    next(err);
  }
};

const testConnection = async (req, res, next) => {
  try {
    const { provider } = req.params;
    const settings = await prisma.aiSettings.findFirst();

    if (!settings) {
      return res.status(400).json({ error: { message: 'No AI settings configured' } });
    }

    const fetch = require('node-fetch');

    switch (provider) {
      case 'openai': {
        if (!settings.openaiApiKey) {
          return res.json({ data: { success: false, message: 'OpenAI API key not set' } });
        }
        const resp = await fetch('https://api.openai.com/v1/models', {
          headers: { Authorization: `Bearer ${settings.openaiApiKey}` },
        });
        res.json({
          data: { success: resp.ok, message: resp.ok ? 'OpenAI connection successful' : `Error: ${resp.status}` },
        });
        break;
      }
      case 'gemini': {
        if (!settings.geminiApiKey) {
          return res.json({ data: { success: false, message: 'Gemini API key not set' } });
        }
        const resp = await fetch(
          `https://generativelanguage.googleapis.com/v1/models?key=${settings.geminiApiKey}`
        );
        res.json({
          data: { success: resp.ok, message: resp.ok ? 'Gemini connection successful' : `Error: ${resp.status}` },
        });
        break;
      }
      case 'openrouter': {
        if (!settings.openrouterApiKey) {
          return res.json({ data: { success: false, message: 'OpenRouter API key not set' } });
        }
        const resp = await fetch('https://openrouter.ai/api/v1/models', {
          headers: { Authorization: `Bearer ${settings.openrouterApiKey}` },
        });
        res.json({
          data: { success: resp.ok, message: resp.ok ? 'OpenRouter connection successful' : `Error: ${resp.status}` },
        });
        break;
      }
      default:
        res.status(400).json({ error: { message: `Unknown provider: ${provider}` } });
    }
  } catch (err) {
    logger.error(`AI connection test failed: ${err.message}`);
    res.json({ data: { success: false, message: err.message } });
  }
};

module.exports = { get, update, testConnection };
