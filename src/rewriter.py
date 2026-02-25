import requests
import os
try:
    from . import config
except ImportError:
    import config

def rewrite_content(content: str, title: str) -> str:
    """Send content to OpenRouter for insightful transformation"""
    
    api_key = os.getenv('OPENROUTER_API_KEY') or config.OPENROUTER_API_KEY
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found.")
        return content  # Return original if no key
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://daily-wiki-insights.github.io",
        "X-Title": "Daily Wiki Insights"
    }
    
    # Use prompt from config
    prompt = config.INSIGHT_PROMPT.format(content=content)
    
    payload = {
        "model": config.REWRITE_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a knowledgeable curator who transforms standard encyclopedia articles into engaging, relevant insights for modern readers. You focus on obscure facts and practical applications."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            config.OPENROUTER_BASE_URL + "/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling OpenRouter: {e}")
        return content # Fallback to original
