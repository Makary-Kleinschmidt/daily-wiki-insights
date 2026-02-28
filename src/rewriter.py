import os
import time
from google import genai
from src import config
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_exception,
)


# --- Gemini API version ---


def _get_gemini_client():
    """Creates and returns a Gemini client with timeout."""
    api_key = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY
    if not api_key:
        print("Warning: GEMINI_API_KEY not found.")
        return None
    # Configure timeout via http_options (in milliseconds)
    timeout_ms = getattr(config, "GEMINI_TIMEOUT", 60) * 1000
    return genai.Client(api_key=api_key, http_options={"timeout": timeout_ms})


# Track exhausted models globally for the session
_exhausted_models = set()


def retry_if_api_error(exception):
    err_msg = str(exception).lower()
    return any(
        code in err_msg
        for code in [
            "503",
            "service unavailable",
            "429",
            "resource_exhausted",
            "504",
            "deadline_exceeded",
        ]
    )


@retry(
    stop=stop_after_attempt(config.MAX_RETRIES + 1),
    wait=wait_exponential(multiplier=1, min=config.RETRY_DELAY, max=60),
    retry=retry_if_exception_type(Exception) & retry_if_exception(retry_if_api_error),
)
def _call_gemini_single_model(
    client, model_name, prompt, system_instruction, temperature, max_tokens
):
    print(f"  🤖 Writing with {model_name}...", flush=True)
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


def _call_gemini_with_fallback(
    prompt, system_instruction, temperature=0.7, max_tokens=2000
):
    """
    Calls Gemini API with model fallback and retries on transient errors.
    Returns the response text or None.
    """
    client = _get_gemini_client()
    if not client:
        return None

    models = getattr(config, "GEMINI_FALLBACK_MODELS", [config.GEMINI_MODEL])

    # Filter out models known to be exhausted in this session
    models = [m for m in models if m not in _exhausted_models]

    if not models:
        print("❌ All configured models are exhausted or unavailable.")
        return None

    for model_name in models:
        if model_name in _exhausted_models:
            continue

        try:
            return _call_gemini_single_model(
                client, model_name, prompt, system_instruction, temperature, max_tokens
            )
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "resource_exhausted" in err_msg:
                print(
                    f"  🚫 {model_name} seems to have hit DAILY LIMIT (or persistent 429). Marking as exhausted."
                )
                _exhausted_models.add(model_name)
            print(
                f"  ❌ Max retries reached or unrecoverable error with {model_name}: {e}. Trying next model..."
            )

    return None


def rewrite_content(content: str, title: str) -> str:
    """Send content to Gemini API for insightful transformation with fallback and retries."""
    prompt = config.INSIGHT_PROMPT.format(content=content)

    result = _call_gemini_with_fallback(
        prompt=prompt,
        system_instruction="You are a knowledgeable curator who transforms standard encyclopedia articles into engaging, relevant insights for modern readers. You focus on obscure facts and practical applications.",
        temperature=0.7,
        max_tokens=2000,
    )

    return result if result else content  # Fallback to original if API fails
