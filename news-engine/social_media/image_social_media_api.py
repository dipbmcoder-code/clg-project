from publication.utils import generate_gemini_image, replace_vars

def generate_tweet_image(twiiter_post, key, l_version, types, website=None):
    custom_prompt = website.get('data', {}).get('social_media_news_image_prompt') if website else None
    
    if custom_prompt:
        prompt_vars = {
            "tweet_text": twiiter_post['tweet_text']
        }
        prompt_text = replace_vars(custom_prompt, prompt_vars)
        prompt = f"Generate a social media image with the following details:\n{prompt_text}"
    elif l_version == 'eng':
        prompt = f"""
        Highly realistic sports breaking news graphic for a major outlet (Sky Sports / BBC Sport / ESPN style), 2025 season.

        Main headline in large, bold white text with subtle red or blue outline: extract the core news from this official announcement and make it short and punchy (max 8–10 words).

        Full quote from the announcement in clean white text box at the bottom third of the image, easy to read.

        Background: ultra-realistic, high-resolution photograph — choose the most relevant scene from:
        • packed football stadium at night with floodlights
        • player holding the new club shirt at official unveiling
        • manager/coach speaking intensely at press conference
        • training ground with players celebrating
        • close-up of player signing contract with club crest visible

        Do NOT use:
        - gradients, digital art, illustrations, cartoons, abstract effects
        - fake newspaper layout, phone screen mockups, or social media borders
        - watermarks, logos, or fake channel bugs

        Colors: dramatic but realistic sports photography tones — keep stadium lights, natural skin tones, authentic kit colors.

        Official announcement to base the graphic on:
        "{twiiter_post['tweet_text']}"

        Image ratio: 1:1 (1024x1024 or 2048x2048), photorealistic, 8K quality, sharp focus, cinematic lighting.
        """
    else:
        prompt = f"Generate a social media image for: {twiiter_post['tweet_text']}"

    generate_gemini_image(prompt, key, l_version, types)

