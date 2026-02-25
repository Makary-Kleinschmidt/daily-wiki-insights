import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
REWRITE_MODEL = "anthropic/claude-sonnet-4"

# Insightful & Relevant Style Prompt
INSIGHT_PROMPT = """Rewrite this Wikipedia article to focus on lesser-known facts and its relevance to modern life.

Rules:
- Start with a "Did you know?" hook containing a surprising or obscure fact from the article.
- Explain the core subject clearly but briefly.
- Dedicate a section to "Why it Matters Today": connect the historical/factual content to modern life, current events, or personal growth.
- Use a tone that is engaging, intellectual, and accessible (like a high-quality newsletter or podcast).
- Avoid academic jargon where possible.
- Length: 300-500 words.

Original content:
{content}

Transform this into an insightful piece:"""
