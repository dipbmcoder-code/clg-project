const prisma = require('../config/database');
const { getPagination, paginatedResponse } = require('../utils/helpers');

const list = async (req, res, next) => {
  try {
    const { skip, take, page, pageSize } = getPagination(req.query);
    const where = {};

    if (req.query.newsType) where.newsType = req.query.newsType;
    if (req.query.newsStatus) where.newsStatus = req.query.newsStatus;
    if (req.query.websiteId) where.websiteId = parseInt(req.query.websiteId);
    if (req.query.search) {
      where.title = { contains: req.query.search, mode: 'insensitive' };
    }

    const [data, total] = await Promise.all([
      prisma.newsLog.findMany({
        where,
        skip,
        take,
        orderBy: { logTime: 'desc' },
        include: { website: { select: { id: true, platformName: true } } },
      }),
      prisma.newsLog.count({ where }),
    ]);

    res.json(paginatedResponse(data, total, { page, pageSize }));
  } catch (err) {
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    const { newsType, title, websiteName, newsStatus, imageGenerated, logMessage, logTime, websiteId } = req.body;
    const log = await prisma.newsLog.create({
      data: {
        newsType,
        title: title || null,
        websiteName: websiteName || null,
        newsStatus: newsStatus || null,
        imageGenerated: imageGenerated || false,
        logMessage: logMessage || null,
        logTime: logTime ? new Date(logTime) : new Date(),
        ...(websiteId && { websiteId }),
      },
    });
    res.status(201).json({ data: log });
  } catch (err) {
    next(err);
  }
};

module.exports = { list, create };
