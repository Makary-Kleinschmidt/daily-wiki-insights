# Changelog - Daily Wiki Insights

All notable changes to this project will be documented in this file.

## [1.1.3] - 2026-02-27

### Changed
- **Model Hierarchy**: Restored `gemini-3-flash-preview` as the primary model and `gemini-2.5-flash` as the first fallback.
- **Fallback Logic**: Configured fallback chain to strictly follow quality tiering: 3.0 -> 2.5 -> 2.0 -> 1.5.

## [1.1.2] - 2026-02-27

### Fixed
- **Short Content Fallback**: Updated `GEMINI_FALLBACK_MODELS` in `config.py` to include a robust list of valid models (`gemini-2.0-flash`, `gemini-2.0-flash-lite-preview-02-05`, `gemini-1.5-flash`, `gemini-1.5-flash-8b`, `gemini-1.5-pro`) to prevent content truncation when primary model quota is exhausted.
- **Model Configuration**: Removed invalid/deprecated model names (`gemini-2.5-flash`, `gemini-3-flash-preview`) from fallback list to avoid unnecessary API errors.

## [1.1.1] - 2026-02-27

### Fixed
- **Short Content Issue**: Switched primary model to `gemini-2.0-flash` to resolve issues with short/truncated content generation due to model quota exhaustion.

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
