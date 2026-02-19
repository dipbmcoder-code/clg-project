const Snoowrap = require('snoowrap');
const logger = require('../config/logger');

class RedditService {
  /**
   * Create a Reddit client from stored credentials
   */
  static createClient(config) {
    return new Snoowrap({
      userAgent: 'ai-news-generator/1.0.0',
      clientId: config.redditClientId,
      clientSecret: config.redditClientSecret,
      username: config.redditUsername,
      password: config.redditPassword,
    });
  }

  /**
   * Post article to configured subreddits
   */
  static async postToReddit(config, { title, articleUrl, subreddits }) {
    const client = this.createClient(config);
    const targetSubs = subreddits || config.redditSubreddits || [];
    const results = [];

    for (const subreddit of targetSubs) {
      try {
        const submission = await client
          .getSubreddit(subreddit)
          .submitLink({
            title: title,
            url: articleUrl,
            resubmit: true,
          });

        logger.info(`Reddit post submitted to r/${subreddit}: ${submission.name}`);
        results.push({
          subreddit,
          success: true,
          postId: submission.name,
          postUrl: `https://reddit.com${submission.permalink}`,
        });
      } catch (err) {
        logger.error(`Reddit post to r/${subreddit} failed: ${err.message}`);
        results.push({
          subreddit,
          success: false,
          error: err.message,
        });
      }
    }

    return results;
  }

  /**
   * Verify Reddit credentials
   */
  static async verifyCredentials(config) {
    try {
      const client = this.createClient(config);
      const me = await client.getMe();
      return { valid: true, username: me.name };
    } catch (err) {
      return { valid: false, error: err.message };
    }
  }
}

module.exports = RedditService;
