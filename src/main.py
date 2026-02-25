import os
import json
from datetime import date
try:
    from .scraper import get_todays_featured_article
    from .rewriter import rewrite_content
except ImportError:
    from scraper import get_todays_featured_article
    from rewriter import rewrite_content
from jinja2 import Template
from dotenv import load_dotenv
import markdown

# Load environment variables
load_dotenv()

import re

def generate_site():
    # 1. Scrape Wikipedia
    print("📚 Fetching Wikipedia TFA...")
    article = get_todays_featured_article()
    
    if not article.get("extract"):
        print("❌ No content found to rewrite.")
        return

    # 2. Rewrite via OpenRouter
    print(f"🧠 Applying insight transformation to '{article['title']}'...")
    insight_content = rewrite_content(article["extract"], article["title"])
    
    # Post-process Markdown to ensure clean rendering
    # Strip whitespace
    insight_content = insight_content.strip()
    # Ensure headers have preceding newlines
    insight_content = re.sub(r'\s*(#{1,6})\s*', r'\n\n\1 ', insight_content)
    # Ensure bold tags have spaces around them if stuck to text (optional, but good for readability)
    # insight_content = re.sub(r'(?<!\s)(\*\*)', r' \1', insight_content) 

    # Convert Markdown to HTML
    print("📝 Converting Markdown to HTML...")
    html_content = markdown.markdown(insight_content, extensions=['extra'])
    
    # 3. Generate HTML
    print("🎨 Generating site...")
    
    # Ensure site directory exists
    os.makedirs("site", exist_ok=True)
    
    template_path = "site/template.html"
    if not os.path.exists(template_path):
        # Fallback if template is not in site/ but in src/ or relative
        # Assuming run from root, site/template.html should be there
        print(f"⚠️ Template not found at {template_path}, checking fallback...")
        if os.path.exists("wikipedia-insights/site/template.html"):
             template_path = "wikipedia-insights/site/template.html"
        elif os.path.exists("brain-rot-wiki/site/template.html"): # Keep for backward compatibility/during transition
             template_path = "brain-rot-wiki/site/template.html"
        else:
             print("❌ Template file not found!")
             # Create a basic template if missing to avoid crash? No, user provided it.
             return

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    
    html = template.render(
        title=article["title"],
        content=html_content,
        image=article.get("thumbnail"),
        wiki_url=article["url"],
        date=date.today().strftime("%B %d, %Y")
    )
    
    output_path = "site/index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # 4. Save metadata for tracking
    with open("site/meta.json", "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": date.today().isoformat(),
            "article": article["title"],
            "source": "wikipedia_tfa"
        }, f)
    
    print(f"✅ Site updated successfully at {output_path}!")

if __name__ == "__main__":
    generate_site()
