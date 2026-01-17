# JLPT Sensei Grammar Scraper

Python scraper to extract Japanese grammar points from [JLPT Sensei](https://jlptsensei.com) website.

## Requirements

- Python 3.13+
- Internet connection

## Installation

```bash
cd scripts
pip install -r requirements.txt
```

## Usage

### Basic Usage (All Levels)

```bash
python run_scraper.py --output ../data/grammar_raw.json
```

### Specific Levels

```bash
python run_scraper.py --levels N5 N4 --output ../data/grammar_raw.json
```

### Test Mode (Limited Items)

```bash
python run_scraper.py --levels N5 --limit 5 --output /tmp/test.json
```

### Custom Request Delay

```bash
python run_scraper.py --delay 2.0
```

## Output Format

The scraper outputs `grammar_raw.json` with this structure:

```json
[
  {
    "id": "grammar-point-slug",
    "title": "Japanese grammar title",
    "titleRomaji": "romaji",
    "explanationEN": "English explanation text",
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
]
```

## Next Steps

After scraping:

1. Review `grammar_raw.json` for completeness
2. Send file to Claude for translation (English → Chinese)
3. Save translated version as `grammar.json`
4. Merge into app's `data/grammar.json`

## Architecture

- **models.py**: Pydantic data models with validation
- **utils.py**: Logging, retry logic, romaji generation, HTTP fetching
- **jlpt_sensei_scraper.py**: Main scraping logic
- **run_scraper.py**: Command-line interface

## Rate Limiting

Default delay: 1.5 seconds between requests to avoid overwhelming the server.

## Error Handling

- Automatic retry (3 attempts) for failed requests
- Validation ensures minimum 2 examples per grammar point
- Detailed logging of all operations
