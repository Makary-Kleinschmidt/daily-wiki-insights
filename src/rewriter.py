import os
import time
from google import genai
try:
    from . import config
except ImportError:
    import config

# --- OpenRouter version (commented out, kept for rollback) ---
# import requests
#
# def rewrite_content_openrouter(content: str, title: str) -> str:
#     """Send content to OpenRouter for insightful transformation"""
#     api_key = os.getenv('OPENROUTER_API_KEY') or config.OPENROUTER_API_KEY
#     if not api_key:
#         print("Warning: OPENROUTER_API_KEY not found.")
#         return content
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://daily-wiki-insights.github.io",
#         "X-Title": "Daily Wiki Insights"
#     }
#     prompt = config.INSIGHT_PROMPT.format(content=content)
#     payload = {
#         "model": config.REWRITE_MODEL,
#         "messages": [
#             {"role": "system", "content": "You are a knowledgeable curator who transforms standard encyclopedia articles into engaging, relevant insights for modern readers. You focus on obscure facts and practical applications."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 1000
#     }
#     try:
#         response = requests.post(config.OPENROUTER_BASE_URL + "/chat/completions", headers=headers, json=payload)
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         print(f"Error calling OpenRouter: {e}")
#         return content

# --- Gemini API version ---

def _get_gemini_client():
    """Creates and returns a Gemini client with timeout."""
    api_key = os.getenv('GEMINI_API_KEY') or config.GEMINI_API_KEY
    if not api_key:
        print("Warning: GEMINI_API_KEY not found.")
        return None
    # Configure timeout via http_options (in milliseconds)
    timeout_ms = getattr(config, 'GEMINI_TIMEOUT', 60) * 1000
    return genai.Client(
        api_key=api_key,
        http_options={'timeout': timeout_ms}
    )


def _call_gemini_with_fallback(prompt, system_instruction, temperature=0.7, max_tokens=2000):
    """
    Calls Gemini API with model fallback and retries on 503 errors.
    Returns the response text or None.
    """
    client = _get_gemini_client()
    if not client:
        return None

    models = getattr(config, 'GEMINI_FALLBACK_MODELS', [config.GEMINI_MODEL])
    
    for model_name in models:
        for attempt in range(config.MAX_RETRIES + 1):
            try:
                print(f"  🤖 Writing with {model_name} (Attempt {attempt + 1})...", flush=True)
                start_time = time.time()
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                )
                duration = time.time() - start_time
                print(f"  ✅ Response received in {duration:.1f}s.", flush=True)
                
                # Rate limit pause after success
                print(f"  ⏳ Rate limit pause ({config.RATE_LIMIT_DELAY}s)...")
                time.sleep(config.RATE_LIMIT_DELAY)
                
                return response.text
            
            except Exception as e:
                err_msg = str(e).lower()
                if "503" in err_msg or "service unavailable" in err_msg or "429" in err_msg:
                    if attempt < config.MAX_RETRIES:
                        print(f"  ⚠️ Service unstable ({e}). Retrying in {config.RETRY_DELAY}s...")
                        time.sleep(config.RETRY_DELAY)
                        continue
                print(f"  ❌ Error with {model_name}: {e}")
                break # Try next model
    
    return None


def rewrite_content(content: str, title: str) -> str:
    """Send content to Gemini API for insightful transformation with fallback and retries."""
    prompt = config.INSIGHT_PROMPT.format(content=content)

    result = _call_gemini_with_fallback(
        prompt=prompt,
        system_instruction="You are a knowledgeable curator who transforms standard encyclopedia articles into engaging, relevant insights for modern readers. You focus on obscure facts and practical applications.",
        temperature=0.7,
        max_tokens=2000
    )

    return result if result else content  # Fallback to original if API fails
