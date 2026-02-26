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

def rewrite_content(content: str, title: str) -> str:
    """Send content to Gemini API for insightful transformation."""

    api_key = os.getenv('GEMINI_API_KEY') or config.GEMINI_API_KEY
    if not api_key:
        print("Warning: GEMINI_API_KEY not found.")
        return content  # Return original if no key

    client = genai.Client(api_key=api_key)

    prompt = config.INSIGHT_PROMPT.format(content=content)

    try:
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction="You are a knowledgeable curator who transforms standard encyclopedia articles into engaging, relevant insights for modern readers. You focus on obscure facts and practical applications.",
                temperature=0.7,
                max_output_tokens=1000,
            ),
        )

        # Rate limiting: 5 RPM
        print(f"  ⏳ Rate limit pause ({config.RATE_LIMIT_DELAY}s)...")
        time.sleep(config.RATE_LIMIT_DELAY)

        return response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return content  # Fallback to original
