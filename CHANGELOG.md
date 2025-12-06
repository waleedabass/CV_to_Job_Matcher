# Changelog

## [Latest] - Gemini AI Integration

### Added
- **Gemini AI Integration**: Added Google Gemini 2.0 Flash (primary) and Gemini 1.5 Flash (fallback) for AI-powered matching
- **Enhanced Semantic Matching**: AI-powered semantic similarity computation using Gemini models
- **Advanced Skill Gap Analysis**: Intelligent skill gap recommendations using AI
- **API Key Management**: Sidebar input for Gemini API key with session persistence
- **Automatic Fallback**: Seamless fallback from Gemini 2.0 Flash to Gemini 1.5 Flash, then to rule-based matching
- **New Module**: `src/gemini_client.py` for Gemini AI interactions

### Changed
- **Matcher Algorithm**: Updated to use AI when available, with rule-based fallback
- **Semantic Similarity Weight**: Increased from 30% to 40% (AI-powered matching is more accurate)
- **Skill Overlap Weight**: Adjusted from 40% to 35% to accommodate AI improvements

### Technical Details
- Primary Model: `gemini-2.0-flash-exp` (experimental, latest)
- Fallback Model: `gemini-1.5-flash` (stable)
- Dependency: Added `google-generativeai>=0.3.0` to requirements.txt

### Usage
1. Get API key from https://aistudio.google.com/apikey
2. Set as environment variable `GOOGLE_AI_API_KEY` or enter in app sidebar
3. App automatically uses AI when key is available
4. Falls back to rule-based matching if API key is not set

### Documentation
- Added `GEMINI_SETUP.md` with detailed setup instructions
- Updated `README.md` with AI integration information

