const prisma = require('../config/database');

// Fields allowed in the NewsPrompt model
const ALLOWED_PROMPT_FIELDS = [
  'previewContentPrompt', 'previewImagePrompt', 'previewRewritePrompt',
  'reviewContentPrompt', 'reviewImagePrompt', 'reviewRewritePrompt',
  'transferContentPrompt', 'transferImagePrompt', 'transferRewritePrompt',
  'rumourContentPrompt', 'rumourImagePrompt', 'rumourRewritePrompt',
  'playerAbroadContentPrompt', 'playerAbroadImagePrompt', 'playerAbroadRewritePrompt',
  'socialMediaContentPrompt', 'socialMediaImagePrompt', 'socialMediaRewritePrompt',
  'whereToWatchContentPrompt', 'whereToWatchImagePrompt', 'whereToWatchRewritePrompt',
  'translationPrompt', 'translationImagePrompt', 'translationRewritePrompt',
];

const get = async (req, res, next) => {
  try {
    let prompt = await prisma.newsPrompt.findFirst();
    if (!prompt) {
      prompt = await prisma.newsPrompt.create({ data: {} });
    }
    res.json({ data: prompt });
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    // Only allow known prompt fields
    const data = {};
    for (const key of ALLOWED_PROMPT_FIELDS) {
      if (req.body[key] !== undefined) data[key] = req.body[key];
    }

    let prompt = await prisma.newsPrompt.findFirst();
    if (!prompt) {
      prompt = await prisma.newsPrompt.create({ data });
    } else {
      prompt = await prisma.newsPrompt.update({
        where: { id: prompt.id },
        data,
      });
    }
    res.json({ data: prompt });
  } catch (err) {
    next(err);
  }
};

module.exports = { get, update };
