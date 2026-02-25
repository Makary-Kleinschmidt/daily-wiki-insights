import requests
from datetime import date

def get_todays_featured_article():
    """Fetch Today's Featured Article from Wikipedia API"""
    today = date.today().isoformat()
    
    # Wikimedia API endpoint for featured content
    endpoint = f"https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{today.replace('-', '/')}"
    
    headers = {
        "User-Agent": "BrainRotWiki/1.0 (https://github.com/example/brain-rot-wiki; contact@example.com)"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching Wikipedia TFA: {response.status_code}")
        return {
            "title": "Error fetching article",
            "extract": "Could not fetch today's featured article.",
            "thumbnail": "",
            "url": ""
        }
        
    data = response.json()
    
    tfa = data.get("tfa", {})
    return {
        "title": tfa.get("titles", {}).get("normalized", "Unknown"),
        "extract": tfa.get("extract", ""),
        "thumbnail": tfa.get("thumbnail", {}).get("source", ""),
        "url": tfa.get("content_urls", {}).get("desktop", {}).get("page", "")
    }
