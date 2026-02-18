"""
AI Image Generation for Social Media Posts
Generates news-style thumbnail images using Gemini/OpenRouter.
Topic-agnostic — adapts based on website's topic_niche setting.
"""
from publication.utils import generate_gemini_image, replace_vars


def generate_post_image(post_data, key, l_version, types, website=None):
    """
    Generate an AI image for a social media post.
    
    Args:
        post_data: Standardized post dict
        key: Unique key for file naming
        l_version: Language version (eng, ru, etc.)
        types: Module type string
        website: Website config dict with prompts and topic_niche
    """
    # Get the post content for the prompt
    post_text = post_data.get("tweet_text", "")
    post_title = post_data.get("post_title", "")
    source = post_data.get("source", "x")
    source_handle = post_data.get("source_handle", "")
    topic = (website.get("topic_niche") or "general news") if website else "general news"

    # Try custom prompt from website config first
    custom_prompt = None
    if website:
        custom_prompt = website.get("social_media_news_image_prompt")

    if custom_prompt:
        prompt_vars = {
            "tweet_text": post_text,
            "post_title": post_title,
            "source": source,
            "source_handle": source_handle,
            "topic_niche": topic,
        }
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a professional news image:\n{prompt_text}"

    else:
        # Default topic-agnostic prompt
        headline = post_title if post_title else post_text[:200]
        prompt = f"""
        Professional, photorealistic news article thumbnail image.
        
        Topic: {topic}
        Headline: "{headline}"
        
        Design requirements:
        - Modern digital news media style (CNN, BBC, Reuters aesthetic)
        - Clean, professional composition with bold typography
        - Main headline text: extract the core news in 6-8 words, large bold white text
        - Relevant background: ultra-realistic photograph matching the topic
        - Color scheme: professional news media tones (dark blues, whites, subtle red accents)
        
        Do NOT use:
        - Gradients, digital art, illustrations, cartoons, or abstract effects
        - Fake newspaper layouts, phone mockups, or social media borders
        - Watermarks, logos, or branding
        
        Image ratio: 1:1 (1024x1024), photorealistic, 8K quality, sharp focus, cinematic lighting.
        """

    generate_gemini_image(prompt, key, l_version, types)


# Keep backward compatibility alias
generate_tweet_image = generate_post_image

