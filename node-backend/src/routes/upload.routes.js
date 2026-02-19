const router = require('express').Router();
const multer = require('multer');
const path = require('path');
const { authenticate } = require('../middleware/auth');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, '../../', process.env.UPLOAD_DIR || 'uploads'));
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
    cb(null, `${uniqueSuffix}${path.extname(file.originalname)}`);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowedExts = /\.(jpeg|jpg|png|gif|webp|svg)$/i;
    const allowedMimes = /^image\/(jpeg|png|gif|webp|svg\+xml)$/;
    const ext = allowedExts.test(path.extname(file.originalname));
    const mime = allowedMimes.test(file.mimetype);
    if (ext && mime) return cb(null, true);
    cb(new Error('Only image files are allowed'));
  },
});

router.post('/', authenticate, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: { message: 'No file uploaded' } });
  }
  res.json({
    data: {
      id: req.file.filename,
      name: req.file.originalname,
      url: `/uploads/${req.file.filename}`,
      size: req.file.size,
      mime: req.file.mimetype,
    },
  });
});

// Multer error handler
router.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ error: { message: err.message } });
  }
  if (err.message === 'Only image files are allowed') {
    return res.status(400).json({ error: { message: err.message } });
  }
  next(err);
});

module.exports = router;
