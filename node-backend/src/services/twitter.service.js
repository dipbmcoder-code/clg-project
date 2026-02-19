const { TwitterApi } = require('twitter-api-v2');
const logger = require('../config/logger');

class TwitterService {
  /**
   * Create a Twitter client from stored credentials
   */
  static createClient(config) {
    return new TwitterApi({
      appKey: config.twitterApiKey,
      appSecret: config.twitterApiSecret,
      accessToken: config.twitterAccessToken,
      accessSecret: config.twitterAccessSecret,
    });
  }

  /**
   * Post a tweet with article link and optional image
   */
  static async postTweet(config, { title, articleUrl, imageUrl, content }) {
    const client = this.createClient(config);
    const rwClient = client.readWrite;

    let tweetText = content || config.postTemplate || '📰 {title}\n\nRead more: {url}';
    tweetText = tweetText.replace('{title}', title).replace('{url}', articleUrl);

    // Trim to Twitter's character limit
    if (tweetText.length > 280) {
      tweetText = tweetText.substring(0, 277) + '...';
    }

    try {
      let mediaId = null;

      // Upload image if provided
      if (imageUrl) {
        try {
          const fetch = require('node-fetch');
          const imageResponse = await fetch(imageUrl);
          const imageBuffer = await imageResponse.buffer();
          mediaId = await rwClient.v1.uploadMedia(imageBuffer, { mimeType: 'image/jpeg' });
        } catch (imgErr) {
          logger.warn(`Failed to upload twitter image: ${imgErr.message}`);
        }
      }

      const tweetPayload = { text: tweetText };
      if (mediaId) {
        tweetPayload.media = { media_ids: [mediaId] };
      }

      const result = await rwClient.v2.tweet(tweetPayload);

      logger.info(`Tweet posted: ${result.data.id}`);
      return {
        success: true,
        postId: result.data.id,
        postUrl: `https://twitter.com/i/status/${result.data.id}`,
      };
    } catch (err) {
      logger.error(`Twitter post failed: ${err.message}`);
      return { success: false, error: err.message };
    }
  }

  /**
   * Verify Twitter credentials
   */
  static async verifyCredentials(config) {
    try {
      const client = this.createClient(config);
      const me = await client.v2.me();
      return { valid: true, username: me.data.username };
    } catch (err) {
      return { valid: false, error: err.message };
    }
  }
}

module.exports = TwitterService;
