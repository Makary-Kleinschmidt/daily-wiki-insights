# Changelog - Daily Wiki Insights

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-02-26

### Added
- **Gemini 3 Flash Preview Integration**: Switched LLM provider from OpenRouter to Google Gemini API using the official `google-genai` SDK.
- **Model Fallback System**: Automated sequence to try `gemini-3-flash-preview` -> `gemini-2.5-flash` -> `gemini-2.0-flash` if preferred models are unavailable.
- **503 Retry Mechanism**: Implemented automatic wait/retry logic (30s delay, 3 retries) for "Service Unavailable" errors during peak load.
- **Improved Rewriting Logic**: Refactored `rewriter.py` with modular Gemini client handling.
- **Rate Limiting**: Integrated 12s rate limiting (5 RPM) to support free-tier API usage.

### Changed
- **Config Architecture**: Updated `config.py` to support tiered model lists and error handling constants.
- **Documentation**: Overhauled README and ARCHITECTURE to reflect the transition to Google's stack.

### Fixed
- Handling of API 529/503 errors through automated fallback.
- Python import path resolution issues in `rewriter.py`.

## [1.0.0] - 2026-02-25
- Initial release using OpenRouter (Claude/GPT) for Wikipedia insight generation.
