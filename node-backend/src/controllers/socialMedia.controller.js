const prisma = require('../config/database');
const TwitterService = require('../services/twitter.service');
const RedditService = require('../services/reddit.service');
const { getPagination, paginatedResponse } = require('../utils/helpers');
const logger = require('../config/logger');

const getConfig = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const wid = parseInt(websiteId, 10);
    if (isNaN(wid)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    let config = await prisma.socialMediaConfig.findUnique({
      where: { websiteId: wid },
    });

    if (!config) {
      config = await prisma.socialMediaConfig.create({
        data: { websiteId: wid },
      });
    }

    // Mask sensitive fields
    const masked = {
      ...config,
      twitterApiKey: config.twitterApiKey ? '••••••••' : null,
      twitterApiSecret: config.twitterApiSecret ? '••••••••' : null,
      twitterAccessToken: config.twitterAccessToken ? '••••••••' : null,
      twitterAccessSecret: config.twitterAccessSecret ? '••••••••' : null,
      twitterBearerToken: config.twitterBearerToken ? '••••••••' : null,
      redditClientSecret: config.redditClientSecret ? '••••••••' : null,
      redditPassword: config.redditPassword ? '••••••••' : null,
      _hasTwitterCreds: !!(config.twitterApiKey && config.twitterApiSecret && config.twitterAccessToken && config.twitterAccessSecret),
      _hasRedditCreds: !!(config.redditClientId && config.redditClientSecret && config.redditUsername && config.redditPassword),
    };

    res.json({ data: masked });
  } catch (err) {
    next(err);
  }
};

const updateConfig = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const wid = parseInt(websiteId, 10);
    if (isNaN(wid)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    const data = { ...req.body };
    // Strip fields that shouldn't be updated directly
    delete data.id;
    delete data.websiteId;
    delete data.createdAt;
    delete data.updatedAt;

    // Don't overwrite with masked values
    const maskedFields = [
      'twitterApiKey', 'twitterApiSecret', 'twitterAccessToken', 'twitterAccessSecret',
      'twitterBearerToken', 'redditClientSecret', 'redditPassword',
    ];
    maskedFields.forEach((field) => {
      if (data[field] && data[field].includes('••••')) delete data[field];
    });

    let config = await prisma.socialMediaConfig.findUnique({
      where: { websiteId: wid },
    });

    if (!config) {
      config = await prisma.socialMediaConfig.create({
        data: { ...data, websiteId: wid },
      });
    } else {
      config = await prisma.socialMediaConfig.update({
        where: { websiteId: wid },
        data,
      });
    }

    logger.info(`Social media config updated for website ${websiteId}`);
    res.json({ data: { message: 'Social media config updated' } });
  } catch (err) {
    next(err);
  }
};

const postToSocial = async (req, res, next) => {
  try {
    const { websiteId, title, articleUrl, imageUrl, platforms, content } = req.body;

    const config = await prisma.socialMediaConfig.findUnique({
      where: { websiteId },
    });

    if (!config) {
      return res.status(404).json({ error: { message: 'Social media not configured for this website' } });
    }

    const results = {};

    // Twitter
    if (platforms.includes('twitter') && config.twitterEnabled) {
      const twitterResult = await TwitterService.postTweet(config, { title, articleUrl, imageUrl, content });

      await prisma.socialMediaPost.create({
        data: {
          platform: 'twitter',
          postId: twitterResult.postId || null,
          postUrl: twitterResult.postUrl || null,
          title,
          articleUrl,
          status: twitterResult.success ? 'posted' : 'failed',
          error: twitterResult.error || null,
          websiteId,
        },
      });

      results.twitter = twitterResult;
    }

    // Reddit
    if (platforms.includes('reddit') && config.redditEnabled) {
      const subreddits = config.redditSubreddits || [];
      const redditResults = await RedditService.postToReddit(config, { title, articleUrl, subreddits });

      for (const r of redditResults) {
        await prisma.socialMediaPost.create({
          data: {
            platform: 'reddit',
            postId: r.postId || null,
            postUrl: r.postUrl || null,
            title,
            content: `Posted to r/${r.subreddit}`,
            articleUrl,
            status: r.success ? 'posted' : 'failed',
            error: r.error || null,
            websiteId,
          },
        });
      }

      results.reddit = redditResults;
    }

    res.json({ data: results });
  } catch (err) {
    next(err);
  }
};

const listPosts = async (req, res, next) => {
  try {
    const { skip, take, page, pageSize } = getPagination(req.query);
    const where = {};

    if (req.query.platform) where.platform = req.query.platform;
    if (req.query.status) where.status = req.query.status;

    const [data, total] = await Promise.all([
      prisma.socialMediaPost.findMany({ where, skip, take, orderBy: { createdAt: 'desc' } }),
      prisma.socialMediaPost.count({ where }),
    ]);

    res.json(paginatedResponse(data, total, { page, pageSize }));
  } catch (err) {
    next(err);
  }
};

const listPostsByWebsite = async (req, res, next) => {
  try {
    const { websiteId } = req.params;
    const wid = parseInt(websiteId, 10);
    if (isNaN(wid)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    const { skip, take, page, pageSize } = getPagination(req.query);

    const where = { websiteId: wid };

    const [data, total] = await Promise.all([
      prisma.socialMediaPost.findMany({ where, skip, take, orderBy: { createdAt: 'desc' } }),
      prisma.socialMediaPost.count({ where }),
    ]);

    res.json(paginatedResponse(data, total, { page, pageSize }));
  } catch (err) {
    next(err);
  }
};

module.exports = { getConfig, updateConfig, postToSocial, listPosts, listPostsByWebsite };
