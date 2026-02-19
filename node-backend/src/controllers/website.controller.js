const prisma = require('../config/database');
const { encrypt, decrypt, getPagination, paginatedResponse } = require('../utils/helpers');
const logger = require('../config/logger');

const list = async (req, res, next) => {
  try {
    const { skip, take, page, pageSize } = getPagination(req.query);
    const where = {};

    // Filters
    if (req.query.active !== undefined) where.active = req.query.active === 'true';
    if (req.query.is_validated !== undefined) where.isValidated = req.query.is_validated === 'true';
    if (req.query.search) {
      where.platformName = { contains: req.query.search, mode: 'insensitive' };
    }

    const [data, total] = await Promise.all([
      prisma.website.findMany({
        where,
        skip,
        take,
        orderBy: { createdAt: 'desc' },
        include: {
          socialMediaConfig: { select: { twitterEnabled: true, redditEnabled: true } },
          _count: { select: { wpCategories: true, newsLogs: true } },
        },
      }),
      prisma.website.count({ where }),
    ]);

    // Mask passwords in response
    const maskedData = data.map((w) => ({
      ...w,
      platformPassword: '••••••••',
    }));

    res.json(paginatedResponse(maskedData, total, { page, pageSize }));
  } catch (err) {
    next(err);
  }
};

const getOne = async (req, res, next) => {
  try {
    const { id } = req.params;
    const websiteId = parseInt(id, 10);
    if (isNaN(websiteId)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    const website = await prisma.website.findUnique({
      where: { id: websiteId },
      include: {
        wpCategories: { orderBy: { name: 'asc' } },
        socialMediaConfig: true,
        manualNews: { include: { manualNews: true } },
      },
    });

    if (!website) {
      return res.status(404).json({ error: { message: 'Website not found' } });
    }

    // Mask sensitive fields
    website.platformPassword = '••••••••';
    if (website.socialMediaConfig) {
      if (website.socialMediaConfig.twitterApiKey) website.socialMediaConfig.twitterApiKey = '••••••••';
      if (website.socialMediaConfig.twitterApiSecret) website.socialMediaConfig.twitterApiSecret = '••••••••';
      if (website.socialMediaConfig.twitterAccessToken) website.socialMediaConfig.twitterAccessToken = '••••••••';
      if (website.socialMediaConfig.twitterAccessSecret) website.socialMediaConfig.twitterAccessSecret = '••••••••';
      if (website.socialMediaConfig.twitterBearerToken) website.socialMediaConfig.twitterBearerToken = '••••••••';
      if (website.socialMediaConfig.redditClientSecret) website.socialMediaConfig.redditClientSecret = '••••••••';
      if (website.socialMediaConfig.redditPassword) website.socialMediaConfig.redditPassword = '••••••••';
    }

    res.json({ data: website });
  } catch (err) {
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    const data = { ...req.body };
    // Strip fields that clients must not set directly
    delete data.id;
    delete data.isValidated;
    delete data.createdAt;
    delete data.updatedAt;
    // Encrypt the WordPress password
    data.platformPassword = encrypt(data.platformPassword);

    const website = await prisma.website.create({ data });
    logger.info(`Website created: ${website.platformName} by user ${req.user.email}`);

    website.platformPassword = '••••••••';
    res.status(201).json({ data: website });
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const websiteId = parseInt(id, 10);
    if (isNaN(websiteId)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    const data = { ...req.body };
    // Strip fields that clients must not set directly
    delete data.id;
    delete data.isValidated;
    delete data.createdAt;
    delete data.updatedAt;

    // If password is being updated and it's not the masked value
    if (data.platformPassword && data.platformPassword !== '••••••••') {
      data.platformPassword = encrypt(data.platformPassword);
    } else {
      delete data.platformPassword;
    }

    const website = await prisma.website.update({
      where: { id: websiteId },
      data,
    });

    website.platformPassword = '••••••••';
    res.json({ data: website });
  } catch (err) {
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    const { id } = req.params;
    const websiteId = parseInt(id, 10);
    if (isNaN(websiteId)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    await prisma.website.delete({ where: { id: websiteId } });
    res.json({ data: { message: 'Website deleted' } });
  } catch (err) {
    next(err);
  }
};

const validateConnection = async (req, res, next) => {
  try {
    const { id } = req.params;
    const websiteId = parseInt(id, 10);
    if (isNaN(websiteId)) {
      return res.status(400).json({ error: { message: 'Invalid website ID' } });
    }
    const website = await prisma.website.findUnique({ where: { id: websiteId } });

    if (!website) {
      return res.status(404).json({ error: { message: 'Website not found' } });
    }

    const password = decrypt(website.platformPassword);
    const fetch = require('node-fetch');
    const auth = Buffer.from(`${website.platformUser}:${password}`).toString('base64');

    const response = await fetch(`${website.platformUrl}/wp-json/wp/v2/users/me`, {
      headers: { Authorization: `Basic ${auth}` },
      timeout: 10000,
    });

    if (response.ok) {
      await prisma.website.update({
        where: { id: websiteId },
        data: { isValidated: true },
      });
      res.json({ data: { valid: true, message: 'WordPress connection successful' } });
    } else {
      await prisma.website.update({
        where: { id: websiteId },
        data: { isValidated: false },
      });
      res.json({ data: { valid: false, message: `WordPress returned status ${response.status}` } });
    }
  } catch (err) {
    logger.error(`WordPress validation error: ${err.message}`);
    res.json({ data: { valid: false, message: err.message } });
  }
};

module.exports = { list, getOne, create, update, remove, validateConnection };
