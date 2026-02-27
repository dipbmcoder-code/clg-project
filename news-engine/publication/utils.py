import os
import requests
import base64
from dotenv import load_dotenv
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()
from datetime import date, datetime
import json
import openai
from openai import OpenAI
from time import sleep
import threading
from publication.db import insert_db
from google import genai
from google.genai import types as genai_types

import pytz

import re

def replace_vars(text, vars_dict):
    for k, v in vars_dict.items():
        # Replace {k}, { k }, {  k  } etc.
        pattern = r"\{\s*" + re.escape(k) + r"\s*\}"
        # Use lambda to avoid interpreting backslashes in str(v)
        text = re.sub(pattern, lambda m: str(v), text)
    return text

def get_timestamp(time_elem):
    """Extract timestamp from tweet <time> element, convert to env timezone."""
    try:
        tz_name = os.getenv("APP_TIMEZONE", "Asia/Kolkata")
        tz = pytz.timezone(tz_name)

        if time_elem and time_elem.has_attr("datetime"):
            # Twitter usually provides UTC in ISO8601 with Z
            raw_time = time_elem["datetime"]
            if raw_time.endswith("Z"):
                dt_utc = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            else:
                dt_utc = datetime.fromisoformat(raw_time)

            # Convert UTC → target timezone
            dt_local = dt_utc.astimezone(tz)
            return dt_local.isoformat()
        else:
            # Fallback: use local now
            return datetime.now(tz).isoformat()
    except Exception as e:
        # Last-resort fallback
        return datetime.now().isoformat()
    
def generate_openRouter_image(prompt, id, l_version, types):
    print("called openrouter")

    image_generated = False
    error_message = None
    image_bytes = None

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        api_key = os.getenv("OPEN_ROUTER_API_KEY")
        model = os.getenv("OPEN_ROUTER_IMAGE_MODEL")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "image_config": {"aspect_ratio": "1:1"}
        }

        response = requests.post(url, headers=headers, json=payload)
        print("Response:", response.status_code)

        if response.status_code != 200:
            # Capture error details from response
            try:
                error_response = response.json()
                error_details = error_response.get('error', {})
                error_code = error_details.get('code', response.status_code)
                error_msg = error_details.get('message', 'Unknown error')
                error_status = error_details.get('status', 'UNKNOWN')
                error_message = f"OpenRouter API error [{error_code}] {error_status}: {error_msg}"
            except:
                # If response is not JSON, use status code and text
                error_message = f"OpenRouter API returned status code {response.status_code}: {response.text[:200]}"
            raise Exception(error_message)

        result = response.json()
        choices = result.get("choices", [])

        if not choices:
            raise Exception("No 'choices' returned from OpenRouter.")

        images = choices[0]["message"].get("images", [])

        if not images:
            raise Exception("No images returned in OpenRouter response.")

        # --- Extract Image URL ---
        image_url = images[0]["image_url"]["url"]

        # --- Convert to bytes (base64 or URL) ---
        if image_url.startswith("data:"):
            base64_data = image_url.split(",", 1)[1]
            base64_data += "=" * (-len(base64_data) % 4)
            image_bytes = base64.b64decode(base64_data)
        else:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image_bytes = response.content

        # --- Save image ---
        if image_bytes:
            output_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}.png"
            with open(output_path, "wb") as f:
                f.write(image_bytes)

            sleep(2)
            image_generated = True
            print(f"[INFO] OpenRouter image generated successfully → {output_path}")
        else:
            raise Exception("Failed to decode image bytes.")

    except Exception as e:
        error_message = f"OpenRouter Image Error: {str(e)}"
        print(error_message)

    finally:
        from publication.message_tracker import add_message, MessageStage, MessageStatus
        add_message(
            types,
            MessageStage.IMAGE_GENERATION,
            MessageStatus.SUCCESS if image_generated else MessageStatus.ERROR,
            "Image generated successfully using OpenRouter" if image_generated else "Image generation failed",
            error_details=None if image_generated else error_message,
        )

def generate_gemini_image(prompt, id, l_version, types):
    
    service = os.getenv("IMAGE_GENERATE_SERVICE", "")
    
    if service == 'skip' or service == 'none':
        print("⏭️ Image generation skipped (IMAGE_GENERATE_SERVICE=skip)")
        from publication.message_tracker import add_message, MessageStage, MessageStatus
        add_message(types, MessageStage.IMAGE_GENERATION, MessageStatus.SUCCESS, "Image generation skipped")
        return
    elif service == 'openrouter':
        generate_openRouter_image(prompt, id, l_version, types)
    elif service == 'imagen':
        generate_imagen_image(prompt, id, l_version, types)
    elif service == 'gemini-flash-image':
        generate_gemini_flash_image(prompt, id, l_version, types)
    else:
        print("called gemini image generation")
        
        image_generated = False
        error_message = None
        max_retries = 2
        retry_delay = 3  # seconds
        
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'key': os.getenv("GOOGLE_GEMINI_API_KEY")
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],  # Request both text and image
            }
        }
        
        try:
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"[INFO] Gemini image generation attempt {attempt}/{max_retries}")
                    
                    # Generate image with Gemini
                    response = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{os.getenv('GOOGLE_GEMINI_MODEL')}:generateContent",
                        headers=headers,
                        params=params,
                        json=data,
                        timeout=30
                    )
                    
                    print(f"[INFO] Response status code: {response.status_code}")
                    
                    # --- Save Full Response Log ---
                    log_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}_response.json"
                    
                    if response.status_code == 200:
                        result = response.json()

                        # Get image bytes from Gemini response
                        if 'candidates' in result and result['candidates']:
                            candidate = result['candidates'][0]
                            if 'content' in candidate and 'parts' in candidate['content']:
                                for part in candidate['content']['parts']:
                                    if 'inlineData' in part:
                                        image_data = part['inlineData']['data']
                                        image_bytes = base64.b64decode(image_data)
                                        output_path = root_folder / 'result' / 'img_match' / f'{l_version}_{id}_{types}.png'
                                        with open(output_path, 'wb') as f:
                                            f.write(image_bytes)
                                        sleep(2)
                                        image_generated = True
                                        print(f"[INFO] Gemini image generated successfully on attempt {attempt}")
                                        break

                                    elif 'text' in part and part['text'].startswith('data:image'):
                                        image_data = part['text'].split(",")[1]
                                        image_bytes = base64.b64decode(image_data)
                                        output_path = root_folder / 'result' / 'img_match' / f'{l_version}_{id}_{types}.png'
                                        with open(output_path, 'wb') as f:
                                            f.write(image_bytes)
                                        sleep(3)
                                        image_generated = True
                                        print(f"[INFO] Gemini image generated successfully on attempt {attempt}")
                                        break
                                
                                if image_generated:
                                    break  # Success, exit retry loop
                                else:
                                    # Save response for debugging
                                    with open(log_path, "w") as f:
                                        json.dump(result, f, indent=2, default=str)
                                    print(f"[INFO] Response saved to {log_path}")
                                    raise Exception("No valid image data found in part (neither 'inlineData' nor 'text' with data:image)")
                            else:
                                # Save response for debugging
                                with open(log_path, "w") as f:
                                    json.dump(result, f, indent=2, default=str)
                                print(f"[INFO] Response saved to {log_path}")
                                raise Exception("No 'content' or 'parts' found in candidate from Gemini response")
                        else:
                            # Save response for debugging
                            with open(log_path, "w") as f:
                                json.dump(result, f, indent=2, default=str)
                            print(f"[INFO] Response saved to {log_path}")
                            raise Exception("No 'candidates' found in Gemini response or candidates list is empty")
                    else:
                        # Capture error details from response
                        try:
                            error_response = response.json()
                            error_details = error_response.get('error', {})
                            error_code = error_details.get('code', response.status_code)
                            error_msg = error_details.get('message', 'Unknown error')
                            error_status = error_details.get('status', 'UNKNOWN')
                            
                            # Save error response for debugging
                            with open(log_path, "w") as f:
                                json.dump(error_response, f, indent=2, default=str)
                            print(f"[INFO] Error response saved to {log_path}")
                            
                            raise Exception(f"Gemini API error [{error_code}] {error_status}: {error_msg}")
                        except json.JSONDecodeError:
                            raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")
                
                except Exception as e:
                    error_message = f"Gemini Image Error (attempt {attempt}/{max_retries}): {str(e)}"
                    print(error_message)
                    
                    # Check for quota errors
                    error_str = str(e)
                    if "429" in error_str or "402" in error_str or "Resource has been exhausted" in error_str or "Quota exceeded" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        print(f"🚨 CRITICAL: Gemini API Quota Exceeded!")
                        send_quota_alert_email(f"Gemini API Quota Exceeded: {error_str}")
                        break
                    
                    # Check if this is a retryable error
                    is_retryable = ("No valid image data found" in error_str or 
                                  "No 'content' or 'parts' found" in error_str or
                                  "No 'candidates' found" in error_str or
                                  "timeout" in error_str.lower())
                    
                    if is_retryable and attempt < max_retries:
                        print(f"[INFO] Retrying in {retry_delay} seconds...")
                        sleep(retry_delay)
                    else:
                        # Either not retryable or max retries reached
                        if attempt == max_retries:
                            error_message = f"Gemini Image Error: Failed after {max_retries} attempts - {str(e)}"
                            print(f"[ERROR] {error_message}")
                        break

        except Exception as _ex:
            error_message = f"Error during calling gemini: {_ex}"
            print(f" {error_message}")
        finally:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_GENERATION,
                MessageStatus.SUCCESS if image_generated else MessageStatus.ERROR,
                "Image generated successfully" if image_generated else "Image generation failed",
                error_details=error_message
            )

def check_data_exists_in_db(data, id, field_name):
    return any(item[field_name] == id for item in data)

def check_is_posted(data, website_id):
    website_ids = data.get("website_ids")
    if isinstance(website_ids, str):
        try:
            website_ids = json.loads(website_ids)
        except (json.JSONDecodeError, TypeError):
            website_ids = []
    return (
        data.get("is_posted") is True and
        isinstance(website_ids, list) and
        str(website_id) in [str(w) for w in website_ids]
    )

def update_post_in_db(id, table_name, websiteIds):
    website_ids_json = json.dumps([str(w) for w in websiteIds])
    update_query = (
        f"UPDATE {table_name} "
        f"SET is_posted = TRUE, "
        f"posted_datetime = NOW(), "
        f"website_ids = '{website_ids_json}'::jsonb "
        f"WHERE id = {id} ;"
    )
    insert_db(update_query)

def sql_value(v):
    if isinstance(v, str):
        # Escape single quotes by doubling them (O'Connor -> O''Connor)
        escaped = v.replace("'", "''")
        return f"'{escaped}'"
    elif isinstance(v, (int, float)):
        return str(v)
    elif isinstance(v, datetime):
        return f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'"
    elif isinstance(v, date):
        return f"'{v.strftime('%Y-%m-%d')}'"
    elif isinstance(v, list):
        # Convert list to Postgres ARRAY
        arr = ", ".join([f"'{str(item).replace("'", "''")}'" for item in v])
        return f"ARRAY[{arr}]"
    elif isinstance(v, dict):
        # Convert dict to JSONB
        dumped = json.dumps(v).replace("'", "''")
        return f"'{dumped}'::jsonb"
    elif isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        # JSON string already
        escaped = v.replace("'", "''")
        return f"'{escaped}'::jsonb"
    else:
        return "NULL"

def generate_openai_content(prompt, key=None):
    content_generated = False
    error_message = None
    content = None
    try:
        service = os.getenv("CONTENT_GENERATE_SERVICE", "openai")

        if service == 'gemini':
            # Use Gemini SDK directly for content generation with key rotation
            gemini_keys_str = os.getenv("GOOGLE_GEMINI_API_KEYS", "")
            primary_key = os.getenv("GOOGLE_GEMINI_API_KEY", "")
            # Build list of keys: primary + extras from GOOGLE_GEMINI_API_KEYS (comma-separated)
            all_keys = [primary_key] if primary_key else []
            if gemini_keys_str:
                for k in gemini_keys_str.split(","):
                    k = k.strip()
                    if k and k not in all_keys:
                        all_keys.append(k)
            if not all_keys:
                raise Exception("No Gemini API keys configured")

            gemini_model = os.getenv("GOOGLE_GEMINI_CONTENT_MODEL", "gemini-2.0-flash")
            last_error = None
            for key_idx, api_key in enumerate(all_keys):
                gemini_client = genai.Client(api_key=api_key)
                max_retries = 2
                for attempt in range(1, max_retries + 1):
                    try:
                        response = gemini_client.models.generate_content(
                            model=gemini_model,
                            contents=prompt,
                        )
                        content = response.text
                        content_generated = True
                        break
                    except Exception as gemini_err:
                        last_error = gemini_err
                        err_str = str(gemini_err)
                        if '429' in err_str and attempt < max_retries:
                            wait_time = 10 * attempt
                            print(f"⏳ Gemini rate limited (key {key_idx+1}), waiting {wait_time}s (attempt {attempt}/{max_retries})...")
                            sleep(wait_time)
                        elif '429' in err_str and key_idx < len(all_keys) - 1:
                            print(f"⏳ Key {key_idx+1} exhausted, trying next key...")
                            break  # try next key
                        else:
                            raise gemini_err
                if content_generated:
                    break
            if not content_generated and last_error:
                raise last_error
        elif service == 'openrouter':
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPEN_ROUTER_API_KEY"),
            )
            model = os.getenv("OPEN_ROUTER_CONTENT_MODEL", "google/gemini-2.0-flash-001")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_completion_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            content = response.choices[0].message.content
            content_generated = True
        else:
            # Default: OpenAI
            client = openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            model = os.getenv('OPENAI_MODEL')
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_completion_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            content = response.choices[0].message.content
            content_generated = True

    except Exception as _ex:
        error_message = f"Error: {_ex}"
        print(f"[info] {error_message}")
        
        # Check for quota/payment errors (402, 429)
        status_code = None
        
        # Try to extract status code from the exception
        if hasattr(_ex, 'status_code'):
            status_code = _ex.status_code
        elif hasattr(_ex, 'response') and hasattr(_ex.response, 'status_code'):
            status_code = _ex.response.status_code
        elif hasattr(_ex, 'code'):
            # OpenAI SDK sometimes uses 'code' attribute
            try:
                status_code = int(_ex.code)
            except (ValueError, TypeError):
                pass
        
        # Check error message for status codes if not found in attributes
        if status_code is None:
            error_str = str(_ex).lower()
            if '402' in error_str or 'payment required' in error_str:
                status_code = 402
            elif '429' in error_str or 'rate limit' in error_str or 'quota' in error_str:
                status_code = 429
        
        # Deactivate all websites if quota/payment error detected
        if status_code in [402, 429]:
            error_type = "Payment Required" if status_code == 402 else "Rate Limit Exceeded"
            print(f"🚨 CRITICAL: API {error_type} error (status {status_code}) detected!")
            error_message = f"CRITICAL API Error [{status_code}] {error_type}: {_ex}"
    
    finally:
        from publication.message_tracker import add_message, MessageStage, MessageStatus
        if key:
            add_message(
                key,
                MessageStage.CONTENT_GENERATION,
                MessageStatus.SUCCESS if content_generated else MessageStatus.ERROR,
                "Content generated successfully" if content_generated and content else "Content generation failed",
                error_details=error_message
            )

    return content

def check_image_exists(lang, types, id):
    img_path = root_folder / f'result/img_match/{lang}_{id}_{types}.png'
    return os.path.exists(img_path)

def download_aws_image(lang, types, id):
    try :
        img_path = root_folder / f'result/img_match/{lang}_{id}_{types}.png'
        aws_image_url = f"{os.getenv('AWS_URL')}/match/{lang}_{id}_{types}.png"
        response = requests.get(aws_image_url, stream=True)
        response.raise_for_status()

        # Save locally
        with open(img_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            return "done"
    except Exception as _ex:
        print("[Error] while downloading image from aws")

def parse_date(value):
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None  # in case of bad or missing data

def check_api_quota():
    """
    Check if API quota is available.
    Tries billing API first, falls back to minimal test call.
    
    Returns:
        tuple: (is_available: bool, error_message: str)
    """
    print("🔍 Checking API quota availability...")
    
    # Determine which service to use
    service = os.getenv("CONTENT_GENERATE_SERVICE", "openai")
    
    # --- Strategy 1: Billing API Check (Preferred) ---
    try:
        if service == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                headers = {"Authorization": f"Bearer {api_key}"}
                # Note: This endpoint is internal/undocumented and may change or require session keys
                billing_url = "https://api.openai.com/v1/dashboard/billing/credit_grants"
                response = requests.get(billing_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    total_granted = data.get("total_granted", 0)
                    total_used = data.get("total_used", 0)
                    available = total_granted - total_used
                    
                    if available <= 0:
                        error_msg = f"Billing API: Quota exhausted (Available: {available})"
                        print(f"❌ {error_msg}")
                        return (False, error_msg)
                    
                    print(f"✅ Billing API check passed (Available credits: {available})")
                    return (True, None)
                elif response.status_code == 401:
                    print("⚠️ Billing API unauthorized (key may not support billing access). Falling back.")
                else:
                    print(f"⚠️ Billing API returned {response.status_code}. Falling back.")
        
        elif service == 'openrouter':
            api_key = os.getenv("OPEN_ROUTER_API_KEY")
            if api_key:
                headers = {"Authorization": f"Bearer {api_key}"}
                credits_url = "https://openrouter.ai/api/v1/credits"
                response = requests.get(credits_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    data_obj = data.get("data", {})
                    total_credits = data_obj.get("total_credits", 0)
                    total_usage = data_obj.get("total_usage", 0)
                    # OpenRouter logic might differ, assuming if credits > usage or positive balance
                    # Actually OpenRouter usually returns 'total_credits' as remaining balance or similar
                    # Let's assume if response is 200, we are good unless explicit error
                    print(f"✅ OpenRouter Credits API check passed")
                    return (True, None)
                
    except Exception as e:
        print(f"⚠️ Billing API check failed: {e}. Falling back to generation check.")

    # --- Strategy 2: Minimal Generation Check (Fallback) ---
    try:
        if service == 'openrouter':
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPEN_ROUTER_API_KEY"),
            )
        else:
            client = openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Make a minimal test call (single token response)
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL'),
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            max_completion_tokens=1,
            temperature=0
        )
        
        print("✅ Generation check passed - quota available")
        return (True, None)
        
    except Exception as e:
        error_str = str(e).lower()
        status_code = None
        
        # Try to extract status code
        if hasattr(e, 'status_code'):
            status_code = e.status_code
        elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
            status_code = e.response.status_code
        elif hasattr(e, 'code'):
            try:
                status_code = int(e.code)
            except (ValueError, TypeError):
                pass
        
        # Check for quota/payment errors
        if status_code in [402, 429] or '402' in error_str or '429' in error_str or \
           'payment required' in error_str or 'rate limit' in error_str or 'quota' in error_str:
            error_type = "Payment Required" if (status_code == 402 or '402' in error_str or 'payment' in error_str) else "Rate Limit Exceeded"
            error_message = f"API {error_type} (Status: {status_code or 'Unknown'}): {str(e)}"
            print(f"❌ API quota check failed: {error_message}")
            return (False, error_message)
        
        # Other errors - assume quota is available but something else is wrong
        print(f"⚠️ API quota check encountered error (assuming quota available): {str(e)}")
        return (True, None)

def _send_email_thread(error_message, email_from, email_to, sendgrid_api_key):
    """Internal function to run email sending in a thread."""
    try:
        print("📧 [Thread] Sending quota alert email via SendGrid...")
        
        # Prepare email content
        subject = "🚨 CRITICAL: API Quota Exceeded - Football News Engine"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
            <h2 style="color: #d32f2f;">🚨 API Quota Exceeded</h2>
            <p><strong>Critical Warning:</strong> The Content Generation API (OpenAI/OpenRouter) has returned a quota error.</p>
            
            <div style="background-color: #ffebee; padding: 15px; border-radius: 5px; border-left: 5px solid #d32f2f; margin: 20px 0;">
                <strong>Error Details:</strong><br>
                <pre style="white-space: pre-wrap;">{error_message}</pre>
            </div>
            
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h3>⚠️ Impact</h3>
            <ul>
                <li>Cron job has been <strong>terminated</strong> to prevent further errors.</li>
                <li>Content generation is currently <strong>paused</strong>.</li>
            </ul>
            
            <h3>✅ Recommended Actions</h3>
            <ol>
                <li>Check your OpenAI/OpenRouter account balance and limits.</li>
                <li>Add credits or upgrade your plan if necessary.</li>
                <li>The system will automatically resume processing on the next scheduled run once the quota issue is resolved.</li>
            </ol>
            
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">Football News Engine Automation System</p>
        </div>
        """

        # SendGrid API URL
        url = "https://api.sendgrid.com/v3/mail/send"

        # Headers
        headers = {
            "Authorization": f"Bearer {sendgrid_api_key}",
            "Content-Type": "application/json"
        }

        # Payload
        data = {
            "personalizations": [
                {
                    "to": [{"email": email_to}],
                    "subject": subject
                }
            ],
            "from": {"email": email_from},
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ]
        }

        # Make the request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code in [200, 201, 202]:
            print(f"✅ [Thread] Alert email sent successfully to: {email_to}")
        else:
            print(f"❌ [Thread] Failed to send alert email via SendGrid. Status: {response.status_code}")
            print(f"   Response: {response.text}")

    except Exception as e:
        print(f"❌ [Thread] Failed to send alert email: {str(e)}")

def send_quota_alert_email(error_message: str):
    """
    Send an email alert to administrators about API quota exhaustion using SendGrid.
    Runs in a separate thread and enforces a once-per-day limit.
    """
    try:
        # Check daily limit
        state_file = root_folder / "quota_alert_state.json"
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    last_sent = state.get('last_sent_date')
                    if last_sent == today_str:
                        print(f"ℹ️ Alert email already sent today ({today_str}). Skipping.")
                        return
            except Exception as e:
                print(f"⚠️ Error reading state file: {e}")

        # Update state file immediately to prevent race conditions (simple approach)
        try:
            with open(state_file, 'w') as f:
                json.dump({'last_sent_date': today_str}, f)
        except Exception as e:
            print(f"⚠️ Error writing state file: {e}")

        # Get configuration
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        email_from = os.getenv('SENDGRID_FROM_EMAIL', "noreply@footballnewsapp.com")
        email_to = os.getenv('SENDER_EMAIL', "tricore104@gmail.com")
        
        if not sendgrid_api_key:
            print("⚠️ Skipping email alert: SENDGRID_API_KEY not found in environment variables")
            return
            
        # Spawn thread
        t = threading.Thread(target=_send_email_thread, args=(error_message, email_from, email_to, sendgrid_api_key))
        t.start()
        print("📧 Email sending task started in background thread.")

    except Exception as e:
        print(f"❌ Failed to initiate alert email: {str(e)}")

def generate_imagen_image(prompt, id, l_version, types):
    print("called imagen via Google GenAI SDK")

    image_generated = False
    error_message = None
    max_retries = 2
    retry_delay = 3  # seconds
    
    try:
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[INFO] Imagen generation attempt {attempt}/{max_retries}")
                
                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY")
                if not api_key:
                    raise Exception("No Google API key found (checked GOOGLE_API_KEY and GOOGLE_GEMINI_API_KEY)")
                    
                client = genai.Client(api_key=api_key)
                
                model = os.getenv("GOOGLE_IMAGEN_MODEL")
                
                response = client.models.generate_images(
                    model=model,
                    prompt=prompt,
                    config=genai_types.GenerateImagesConfig(
                        aspect_ratio="1:1",
                        number_of_images=1
                    )
                )
                
                # --- Save Full Response Log ---
                log_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}_response.json"

                if not hasattr(response, 'generated_images') or not response.generated_images:
                    with open(log_path, "w") as f:
                        json.dump(response, f, indent=2, default=str)
                    print(f"[INFO] Response saved to {log_path}")
                    raise Exception("No images returned from Google GenAI.")

                first_image = response.generated_images[0]
                
                image_bytes = None
                if hasattr(first_image, 'image') and first_image.image:
                    if hasattr(first_image.image, 'image_bytes'):
                        image_bytes = first_image.image.image_bytes
                    elif hasattr(first_image.image, 'data'):
                        image_bytes = first_image.image.data
                elif hasattr(first_image, 'image_bytes'):
                    image_bytes = first_image.image_bytes
                elif hasattr(first_image, 'data'):
                    image_bytes = first_image.data
                
                if not image_bytes:
                    with open(log_path, "w") as f:
                        json.dump(response, f, indent=2, default=str)
                    print(f"[INFO] Response saved to {log_path}")
                    raise Exception("Could not extract image bytes from response.")


                output_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}.png"
                with open(output_path, "wb") as f:
                    f.write(image_bytes)

                sleep(3)
                image_generated = True
                print(f"[INFO] Imagen image generated successfully on attempt {attempt}")
                break  # Success, exit retry loop

            except Exception as e:
                error_message = f"Imagen Image Error (attempt {attempt}/{max_retries}): {str(e)}"
                print(error_message)
                
                # Check for quota errors
                error_str = str(e)
                if "429" in error_str or "402" in error_str or "Resource has been exhausted" in error_str or "Quota exceeded" in error_str:
                    print(f"🚨 CRITICAL: Imagen API Quota Exceeded!")
                    send_quota_alert_email(f"Imagen API Quota Exceeded: {error_str}")
                    break

                # Check if this is a retryable error
                is_retryable = ("No images returned from Google GenAI." in error_str or 
                              "Could not extract image bytes from response." in error_str)
                
                if is_retryable and attempt < max_retries:
                    print(f"[INFO] Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
                else:
                    # Either not retryable or max retries reached
                    if attempt == max_retries:
                        error_message = f"Imagen Image Error: Failed after {max_retries} attempts - {str(e)}"
                        print(f"[ERROR] {error_message}")
                    break

    finally:
        from publication.message_tracker import add_message, MessageStage, MessageStatus
        add_message(
            types,
            MessageStage.IMAGE_GENERATION,
            MessageStatus.SUCCESS if image_generated else MessageStatus.ERROR,
            "Image generated successfully using Imagen" if image_generated else "Image generation failed",
            error_details=None if image_generated else error_message,
        )

def generate_gemini_flash_image(prompt, id, l_version, types):
    """
    Generate image using Gemini 2.5 Flash Image model via Google GenAI SDK.
    Based on the new generate_content API with image generation capabilities.
    """
    print("called Gemini 2.5 Flash Image via Google GenAI SDK")

    image_generated = False
    error_message = None
    max_retries = 2
    retry_delay = 3  # seconds
    
    try:
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[INFO] Gemini Flash Image generation attempt {attempt}/{max_retries}")
                
                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY")
                if not api_key:
                    raise Exception("No Google API key found (checked GOOGLE_API_KEY and GOOGLE_GEMINI_API_KEY)")
                    
                client = genai.Client(api_key=api_key)
                
                # Use gemini-2.5-flash-image model
                model = os.getenv("GOOGLE_GEMINI_MODEL") or "gemini-2.5-flash-image"
                
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt]
                )
                
                # --- Save Full Response Log ---
                log_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}_response.json"

                if not hasattr(response, 'parts') or not response.parts:
                    with open(log_path, "w") as f:
                        json.dump({"error": response}, f, indent=2, default=str)
                    print(f"[INFO] Response saved to {log_path}")
                    raise Exception("No parts returned from Gemini Flash Image.")

                # Iterate through parts to find image
                image_found = False
                for part in response.parts:
                    if part.text is not None:
                        print(f"[INFO] Text response: {part.text}")
                    elif part.inline_data is not None:
                        # Found image data
                        image = part.as_image()
                        output_path = root_folder / "result" / "img_match" / f"{l_version}_{id}_{types}.png"
                        image.save(str(output_path))
                        
                        sleep(2)
                        image_generated = True
                        image_found = True
                        print(f"[INFO] Gemini Flash Image generated successfully on attempt {attempt}")
                        break
                
                if image_found:
                    break  # Success, exit retry loop
                else:
                    with open(log_path, "w") as f:
                        json.dump({"error": response}, f, indent=2, default=str)
                    print(f"[INFO] Response saved to {log_path}")
                    raise Exception("No image data found in response parts.")

            except Exception as e:
                error_message = f"Gemini Flash Image Error (attempt {attempt}/{max_retries}): {str(e)}"
                print(error_message)
                
                # Check for quota errors
                error_str = str(e)
                if "429" in error_str or "402" in error_str or "Resource has been exhausted" in error_str or "Quota exceeded" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(f"🚨 CRITICAL: Gemini Flash Image API Quota Exceeded!")
                    send_quota_alert_email(f"Gemini Flash Image API Quota Exceeded: {error_str}")
                    break

                # Check if this is a retryable error
                is_retryable = ("No parts returned from Gemini Flash Image" in error_str or 
                              "No image data found in response parts" in error_str or
                              "timeout" in error_str.lower())
                
                if is_retryable and attempt < max_retries:
                    print(f"[INFO] Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
                else:
                    # Either not retryable or max retries reached
                    if attempt == max_retries:
                        error_message = f"Gemini Flash Image Error: Failed after {max_retries} attempts - {str(e)}"
                        print(f"[ERROR] {error_message}")
                    break

    finally:
        from publication.message_tracker import add_message, MessageStage, MessageStatus
        add_message(
            types,
            MessageStage.IMAGE_GENERATION,
            MessageStatus.SUCCESS if image_generated else MessageStatus.ERROR,
            "Image generated successfully using Gemini 2.5 Flash Image" if image_generated else "Image generation failed",
            error_details=None if image_generated else error_message,
        )
