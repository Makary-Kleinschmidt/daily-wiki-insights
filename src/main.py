import os
import json
from datetime import date
from pathlib import Path
from src.scraper import get_todays_featured_article
from src.rewriter import rewrite_content
from jinja2 import Template
from dotenv import load_dotenv
import markdown
import re

# Load environment variables
load_dotenv()

def generate_site():
    # 1. Scrape Wikipedia
    print("📚 Fetching Wikipedia TFA...")
    article = get_todays_featured_article()
    
    if not article.get("extract"):
        print("❌ No content found to rewrite.")
        return

    # 2. Rewrite via LLM
    print(f"🧠 Applying insight transformation to '{article['title']}'...")
    insight_content = rewrite_content(article["extract"], article["title"])
    
    # Post-process Markdown to ensure clean rendering
    # Strip whitespace
    insight_content = insight_content.strip()
    # Ensure headers have preceding newlines
    insight_content = re.sub(r'\s*(#{1,6})\s*', r'\n\n\1 ', insight_content)

    # Convert Markdown to HTML
    print("📝 Converting Markdown to HTML...")
    html_content = markdown.markdown(insight_content, extensions=['extra'])
    
    # 3. Generate HTML
    print("🎨 Generating site...")
    
    # Path resolution using pathlib
    BASE_DIR = Path(__file__).parent.parent
    site_dir = BASE_DIR / "site"
    site_dir.mkdir(exist_ok=True)
    
    template_path = site_dir / "template.html"
    if not template_path.exists():
        print(f"❌ Template file not found at {template_path}!")
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
    
    output_path = site_dir / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # 4. Save metadata for tracking
    meta_path = site_dir / "meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": date.today().isoformat(),
            "article": article["title"],
            "source": "wikipedia_tfa"
        }, f)
    
    print(f"✅ Site updated successfully at {output_path}!")

if __name__ == "__main__":
    generate_site()
