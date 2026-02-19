const prisma = require('../config/database');
const { getPagination, paginatedResponse } = require('../utils/helpers');

const list = async (req, res, next) => {
  try {
    const { skip, take, page, pageSize } = getPagination(req.query);
    const where = {};

    if (req.query.newsType) where.newsType = req.query.newsType;

    const [data, total] = await Promise.all([
      prisma.manualNews.findMany({
        where,
        skip,
        take,
        orderBy: { createdAt: 'desc' },
        include: {
          websites: { include: { website: { select: { id: true, platformName: true } } } },
          websiteNews: true,
        },
      }),
      prisma.manualNews.count({ where }),
    ]);

    res.json(paginatedResponse(data, total, { page, pageSize }));
  } catch (err) {
    next(err);
  }
};

const getOne = async (req, res, next) => {
  try {
    const { id } = req.params;
    const newsId = parseInt(id, 10);
    if (isNaN(newsId)) {
      return res.status(400).json({ error: { message: 'Invalid ID' } });
    }
    const news = await prisma.manualNews.findUnique({
      where: { id: newsId },
      include: {
        websites: { include: { website: true } },
        websiteNews: true,
      },
    });

    if (!news) {
      return res.status(404).json({ error: { message: 'Manual news not found' } });
    }

    res.json({ data: news });
  } catch (err) {
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    const { websiteIds, ...newsData } = req.body;

    const news = await prisma.manualNews.create({
      data: {
        ...newsData,
        ...(websiteIds && {
          websites: {
            create: websiteIds.map((wid) => ({ websiteId: wid })),
          },
        }),
      },
      include: { websites: true },
    });

    res.status(201).json({ data: news });
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const newsId = parseInt(id, 10);
    if (isNaN(newsId)) {
      return res.status(400).json({ error: { message: 'Invalid ID' } });
    }
    const { websiteIds, ...newsData } = req.body;

    // Use transaction to prevent data loss if update fails after delete
    const news = await prisma.$transaction(async (tx) => {
      if (websiteIds) {
        await tx.manualNewsWebsite.deleteMany({ where: { manualNewsId: newsId } });
      }
      return tx.manualNews.update({
        where: { id: newsId },
        data: {
          ...newsData,
          ...(websiteIds && {
            websites: {
              create: websiteIds.map((wid) => ({ websiteId: wid })),
            },
          }),
        },
        include: { websites: true, websiteNews: true },
      });
    });

    res.json({ data: news });
  } catch (err) {
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    const { id } = req.params;
    const newsId = parseInt(id, 10);
    if (isNaN(newsId)) {
      return res.status(400).json({ error: { message: 'Invalid ID' } });
    }
    await prisma.manualNews.delete({ where: { id: newsId } });
    res.json({ data: { message: 'Manual news deleted' } });
  } catch (err) {
    next(err);
  }
};

module.exports = { list, getOne, create, update, remove };
