# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A personal web application for learning Japanese grammar through random exposure and spaced practice. The project consists of:
1. **Frontend web app** - Pure HTML/CSS/JavaScript (no frameworks or build tools)
2. **Python scraper** - Extracts grammar data from JLPT Sensei website

## Commands

### Running the Web App
```bash
# Open in browser (no build step needed)
open index.html
```

### Python Scraper (scripts directory)

**Setup:**
```bash
cd scripts
pip install -r requirements.txt
```

**Scrape all JLPT levels:**
```bash
python run_scraper.py --output ../data/grammar_raw.json
```

**Scrape specific levels:**
```bash
python run_scraper.py --levels N5 N4 --output ../data/grammar_raw.json
```

**Test mode (limited items):**
```bash
python run_scraper.py --levels N5 --limit 5 --output /tmp/test.json
```

**Custom request delay:**
```bash
python run_scraper.py --delay 2.0
```

## Architecture

### Frontend App Structure (Root Directory)

- **index.html** (37 lines) - Main application page, minimal structure
- **app.js** (323 lines) - All application logic in `GrammarApp` class
- **styles.css** (400 lines) - Styling and responsive design
- **data/grammar.json** - Grammar points database (Chinese translations)

**Key Design Patterns:**
- Single `GrammarApp` class manages all state and behavior
- localStorage for persistence (masteredGrammar Set stored as JSON array)
- Two views: `'card'` (single grammar) and `'list'` (all grammar)
- Smart random selection prioritizes non-mastered items (80% probability)

**Data Flow:**
1. Load grammar from `data/grammar.json`
2. Load mastery state from localStorage
3. Display random grammar (prioritizing non-mastered)
4. User marks as mastered → save to localStorage
5. Update progress counter

### Python Scraper Structure (scripts/)

```
scripts/
├── run_scraper.py              # CLI entry point
├── requirements.txt            # Dependencies
└── scraper/
    ├── __init__.py
    ├── models.py               # Pydantic data models
    ├── utils.py                # Logging, retry, romaji, HTTP
    └── jlpt_sensei_scraper.py  # Main scraping logic
```

**Scraper Pipeline:**
1. Fetch JLPT level index page
2. Extract grammar point URLs
3. For each URL: fetch page, extract title/explanation/examples
4. Generate romaji using pykakasi
5. Validate with Pydantic (min 2 examples required)
6. Output to `grammar_raw.json`

**Post-Scraping Workflow:**
1. Review `grammar_raw.json` for completeness
2. Send to Claude for translation (English → Chinese)
3. Save translated version as `grammar.json`
4. Merge into app's `data/grammar.json`

## Grammar Data Format

**Scraper Output (`grammar_raw.json`):**
```json
{
  "id": "grammar-point-slug",
  "title": "Japanese grammar title",
  "titleRomaji": "romaji",
  "explanationEN": "English explanation",
  "examples": [
    {
      "japanese": "日本語例文",
      "romaji": "Nihongo reibun",
      "englishTranslation": "English translation"
    }
  ],
  "jlptLevel": "N5",
  "source": "JLPT Sensei",
  "url": "https://jlptsensei.com/..."
}
```

**App Format (`data/grammar.json`):**
```json
{
  "id": "unique-id",
  "title": "Japanese Title",
  "titleRomaji": "romaji",
  "explanation": "Chinese explanation",
  "examples": [
    {
      "japanese": "日本語の例",
      "romaji": "Nihongo no rei",
      "english": "Chinese translation"
    }
  ],
  "jlptLevel": "N5",
  "source": "JLPT Sensei",
  "url": "https://jlptsensei.com/..."
}
```

## Key Implementation Details

### Mastery Tracking Logic (app.js)
- Mastered grammar stored in localStorage as JSON array
- Loaded into Set for O(1) lookups
- Random selection uses weighted probability (80% non-mastered, 20% mastered)
- Progress footer shows `mastered/total` ratio

### Keyboard Shortcuts
- `Space` - Show random grammar
- `M` - Toggle mastery for current grammar

### Scraper Rate Limiting
- Default delay: 1.5 seconds between requests
- Automatic retry (3 attempts) for failed requests
- Respects robots.txt and avoids overwhelming server

### Romaji Generation
Uses pykakasi library to convert Japanese text to romanized form automatically.

## Project Status

The app is feature-complete for personal use. The scraper successfully extracted 141 JLPT grammar points from JLPT Sensei.

**Future Enhancement Ideas:**
- Practice exercises (fill-in-the-blank, multiple choice)
- Grammar categories and filtering
- Export/import progress
- Study statistics and streaks
- Spaced repetition algorithm
