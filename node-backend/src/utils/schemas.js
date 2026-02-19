const { z } = require('zod');

// ─── Auth Schemas ────────────────────────────────────────────
const loginSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
  }),
});

const registerSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    firstName: z.string().min(1, 'First name is required'),
    lastName: z.string().min(1, 'Last name is required'),
    role: z.enum(['SUPER_ADMIN', 'ADMIN', 'AGENT']).optional(),
  }),
});

const userUpdateSchema = z.object({
  body: z.object({
    email: z.string().email().optional(),
    password: z.string().min(8).optional(),
    firstName: z.string().min(1).optional(),
    lastName: z.string().min(1).optional(),
    role: z.enum(['SUPER_ADMIN', 'ADMIN', 'AGENT']).optional(),
    isActive: z.boolean().optional(),
  }),
});

// ─── Website Schemas ─────────────────────────────────────────
const websiteSchema = z.object({
  body: z.object({
    platformName: z.string().min(1, 'Platform name is required'),
    platformUrl: z.string().url('Invalid URL'),
    platformUser: z.string().min(1, 'Username is required'),
    platformPassword: z.string().min(1, 'Password is required'),
    websiteAuthor: z.string().optional(),
    active: z.boolean().optional(),
    typeStatus: z.enum(['publish', 'draft']).optional(),
    featuredImage: z.enum(['upload', 'url', 'fifu']).optional(),
    language: z.enum(['eng', 'ru']).optional(),
    enableMatchReviews: z.boolean().optional(),
    enableMatchPreviews: z.boolean().optional(),
    enableSocialMedia: z.boolean().optional(),
    enablePlayerAbroad: z.boolean().optional(),
    enablePlayerProfiles: z.boolean().optional(),
    enableTransferRumors: z.boolean().optional(),
    enableWhereToWatch: z.boolean().optional(),
    websiteLeagues: z.any().optional(),
    platformCountries: z.any().optional(),
    twitterHandles: z.any().optional(),
    openaiPrompt: z.string().optional(),
  }).strip(),
});

const websiteUpdateSchema = z.object({
  body: z.object({
    platformName: z.string().min(1).optional(),
    platformUrl: z.string().url().optional(),
    platformUser: z.string().min(1).optional(),
    platformPassword: z.string().optional(),
    websiteAuthor: z.string().optional(),
    active: z.boolean().optional(),
    typeStatus: z.enum(['publish', 'draft']).optional(),
    featuredImage: z.enum(['upload', 'url', 'fifu']).optional(),
    language: z.enum(['eng', 'ru']).optional(),
    enableMatchReviews: z.boolean().optional(),
    enableMatchPreviews: z.boolean().optional(),
    enableSocialMedia: z.boolean().optional(),
    enablePlayerAbroad: z.boolean().optional(),
    enablePlayerProfiles: z.boolean().optional(),
    enableTransferRumors: z.boolean().optional(),
    enableWhereToWatch: z.boolean().optional(),
    websiteLeagues: z.any().optional(),
    platformCountries: z.any().optional(),
    twitterHandles: z.any().optional(),
    openaiPrompt: z.string().optional(),
  }).strip(),
});

// ─── News Prompt Schema ──────────────────────────────────────
const newsPromptSchema = z.object({
  body: z.object({
    previewContentPrompt: z.string().optional(),
    previewImagePrompt: z.string().optional(),
    previewRewritePrompt: z.string().optional(),
    reviewContentPrompt: z.string().optional(),
    reviewImagePrompt: z.string().optional(),
    reviewRewritePrompt: z.string().optional(),
    transferContentPrompt: z.string().optional(),
    transferImagePrompt: z.string().optional(),
    transferRewritePrompt: z.string().optional(),
    rumourContentPrompt: z.string().optional(),
    rumourImagePrompt: z.string().optional(),
    rumourRewritePrompt: z.string().optional(),
    playerAbroadContentPrompt: z.string().optional(),
    playerAbroadImagePrompt: z.string().optional(),
    playerAbroadRewritePrompt: z.string().optional(),
    socialMediaContentPrompt: z.string().optional(),
    socialMediaImagePrompt: z.string().optional(),
    socialMediaRewritePrompt: z.string().optional(),
    whereToWatchContentPrompt: z.string().optional(),
    whereToWatchImagePrompt: z.string().optional(),
    whereToWatchRewritePrompt: z.string().optional(),
    translationPrompt: z.string().optional(),
    translationImagePrompt: z.string().optional(),
    translationRewritePrompt: z.string().optional(),
  }).strip(),
});

// ─── Manual News Schema ──────────────────────────────────────
const manualNewsSchema = z.object({
  body: z.object({
    newsType: z.enum(['match_reviews', 'match_previews']),
    homeTeam: z.string().optional(),
    awayTeam: z.string().optional(),
    homeScore: z.number().optional(),
    awayScore: z.number().optional(),
    league: z.any().optional(),
    summary: z.string().optional(),
    venue: z.string().optional(),
    websiteIds: z.array(z.number()).optional(),
  }).strip(),
});

// ─── News Log Schema ─────────────────────────────────────────
const newsLogSchema = z.object({
  body: z.object({
    newsType: z.string().min(1, 'News type is required'),
    title: z.string().optional(),
    websiteName: z.string().optional(),
    newsStatus: z.string().optional(),
    imageGenerated: z.boolean().optional(),
    logMessage: z.any().optional(),
    logTime: z.string().optional(),
    websiteId: z.number().int().optional(),
  }).strip(),
});

// ─── AI Settings Schema ──────────────────────────────────────
const aiSettingsSchema = z.object({
  body: z.object({
    openaiApiKey: z.string().optional(),
    openaiModel: z.string().optional(),
    openrouterApiKey: z.string().optional(),
    openrouterModel: z.string().optional(),
    geminiApiKey: z.string().optional(),
    geminiModel: z.string().optional(),
    contentService: z.enum(['openai', 'openrouter']).optional(),
    imageService: z.enum(['gemini', 'openrouter', 'imagen', 'gemini-flash-image']).optional(),
    rapidapiKey: z.string().optional(),
    awsAccessKey: z.string().optional(),
    awsSecretKey: z.string().optional(),
    awsS3Bucket: z.string().optional(),
    awsRegion: z.string().optional(),
    sendgridApiKey: z.string().optional(),
    alertEmail: z.string().email().optional().or(z.literal('')),
  }).strip(),
});

// ─── Social Media Config Schema ──────────────────────────────
const socialMediaConfigSchema = z.object({
  body: z.object({
    twitterEnabled: z.boolean().optional(),
    twitterApiKey: z.string().optional(),
    twitterApiSecret: z.string().optional(),
    twitterAccessToken: z.string().optional(),
    twitterAccessSecret: z.string().optional(),
    twitterBearerToken: z.string().optional(),
    redditEnabled: z.boolean().optional(),
    redditClientId: z.string().optional(),
    redditClientSecret: z.string().optional(),
    redditUsername: z.string().optional(),
    redditPassword: z.string().optional(),
    redditSubreddits: z.array(z.string()).optional(),
    autoPostOnPublish: z.boolean().optional(),
    postTemplate: z.string().optional(),
  }).strip(),
});

// ─── Social Media Post Schema ────────────────────────────────
const socialMediaPostSchema = z.object({
  body: z.object({
    websiteId: z.number(),
    title: z.string().min(1),
    articleUrl: z.string().url(),
    imageUrl: z.string().optional(),
    platforms: z.array(z.enum(['twitter', 'reddit'])).min(1),
    content: z.string().optional(),
  }),
});

module.exports = {
  loginSchema,
  registerSchema,
  userUpdateSchema,
  websiteSchema,
  websiteUpdateSchema,
  newsPromptSchema,
  manualNewsSchema,
  newsLogSchema,
  aiSettingsSchema,
  socialMediaConfigSchema,
  socialMediaPostSchema,
};
