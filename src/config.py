import os

# --- OpenRouter (commented out, kept for rollback) ---
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# REWRITE_MODEL = "deepseek/deepseek-v3.2"

# --- Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.0-flash"
RATE_LIMIT_DELAY = 12  # seconds between calls (5 RPM limit)
DAILY_LIMIT = 20       # max 20 requests per day

# Insightful & Relevant Style Prompt
INSIGHT_PROMPT = """You are an expert content creator and intellectual newsletter author. You excel at transforming factual information into captivating narratives.

Your task is to rewrite the provided Wikipedia article into a highly engaging, insightful piece (300-500 words). Focus on lesser-known facts and connect the subject to modern life.

IMPORTANT FORMATTING RULES:
1. Use standard Markdown formatting.
2. Use "##" for section headers.
3. ALWAYS put a blank line before and after every header.
4. bold key phrases using "**bold**".
5. Do not use the article title as the first header; start directly with the hook.

Structure your response as follows:

## The Hook
Start with a "Did you know?" paragraph containing a surprising fact.

## The Story
Provide a clear, brief explanation of the core subject, focusing on the narrative arc or key conflict.

## Why It Matters Today
A dedicated section connecting the content to modern life, current events, or personal growth.

Input Text:
{content}
"""
