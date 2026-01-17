# JLPT Sensei Scraper Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python web scraper to extract 150-180 Japanese grammar points from JLPT Sensei (N5-N2 levels) with automatic romaji generation, outputting structured JSON data for later translation.

**Architecture:** Three-component system with a main scraper module (list + detail page parsing), a utilities module (logging, retry logic, rate limiting), and a data models module (Pydantic validation). Output is grammar_raw.json containing English explanations that will be manually translated to Chinese later.

**Tech Stack:** Python 3.13, requests (HTTP), BeautifulSoup4 (HTML parsing), pykakasi (romaji generation), Pydantic (data validation)

---

## Task 1: Project Structure and Dependencies

**Files:**
- Create: `scripts/scraper/__init__.py`
- Create: `scripts/scraper/models.py`
- Create: `scripts/scraper/utils.py`
- Create: `scripts/scraper/jlpt_sensei_scraper.py`
- Create: `scripts/run_scraper.py`
- Create: `scripts/requirements.txt`

**Step 1: Create directory structure**

```bash
mkdir -p scripts/scraper
touch scripts/scraper/__init__.py
```

Expected: Directories and __init__.py created

**Step 2: Create requirements.txt**

Create `scripts/requirements.txt`:

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
pykakasi>=2.2.1
pydantic>=2.5.0
```

**Step 3: Test dependency installation**

```bash
cd scripts
python3.13 -m pip install -r requirements.txt
```

Expected: All packages install successfully

**Step 4: Commit**

```bash
git add scripts/
git commit -m "feat: add scraper project structure and dependencies"
```

---

## Task 2: Data Models

**Files:**
- Create: `scripts/scraper/models.py`

**Step 1: Write example usage test**

Create `scripts/scraper/models.py` with test at bottom:

```python
from pydantic import BaseModel, field_validator
from typing import List


class Example(BaseModel):
    """Single example sentence with translations."""
    japanese: str
    romaji: str
    englishTranslation: str

    @field_validator('japanese', 'romaji', 'englishTranslation')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class GrammarPoint(BaseModel):
    """Complete grammar point with metadata."""
    id: str
    title: str
    titleRomaji: str
    explanationEN: str
    examples: List[Example]
    jlptLevel: str
    source: str = "JLPT Sensei"
    url: str

    @field_validator('examples')
    @classmethod
    def min_examples(cls, v: List[Example]) -> List[Example]:
        if len(v) < 2:
            raise ValueError('Must have at least 2 examples')
        return v

    @field_validator('jlptLevel')
    @classmethod
    def valid_level(cls, v: str) -> str:
        if v not in ['N5', 'N4', 'N3', 'N2', 'N1']:
            raise ValueError(f'Invalid JLPT level: {v}')
        return v


# Test the models work
if __name__ == '__main__':
    example = Example(
        japanese="これは本です。",
        romaji="Kore wa hon desu.",
        englishTranslation="This is a book."
    )

    grammar = GrammarPoint(
        id="test-grammar",
        title="は (wa)",
        titleRomaji="wa",
        explanationEN="Topic marker particle",
        examples=[example, example],
        jlptLevel="N5",
        url="https://example.com"
    )

    print("Models validated successfully!")
    print(f"Grammar: {grammar.title}")
```

**Step 2: Run test**

```bash
cd scripts
python3.13 scraper/models.py
```

Expected: Output "Models validated successfully!" and "Grammar: は (wa)"

**Step 3: Commit**

```bash
git add scripts/scraper/models.py
git commit -m "feat: add Pydantic data models with validation"
```

---

## Task 3: Utility Functions

**Files:**
- Create: `scripts/scraper/utils.py`

**Step 1: Write logging setup and retry decorator**

Create `scripts/scraper/utils.py`:

```python
import logging
import time
from functools import wraps
from typing import Callable, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('jlpt_scraper')


def retry(max_attempts: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )

            raise last_exception

        return wrapper
    return decorator


def slugify(text: str) -> str:
    """Convert Japanese grammar title to URL-safe slug."""
    import re
    # Remove special characters but keep letters, numbers, spaces, and Japanese
    text = re.sub(r'[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text.strip())
    # Lowercase
    return text.lower()


# Test utilities
if __name__ == '__main__':
    # Test slugify
    assert slugify("は (wa) - Topic Marker") == "は-wa-topic-marker"
    print("✓ slugify works")

    # Test retry
    attempt_count = 0

    @retry(max_attempts=3, delay=0.1, backoff=1.5)
    def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise ValueError("Temporary failure")
        return "success"

    result = flaky_function()
    assert result == "success"
    assert attempt_count == 2
    print("✓ retry decorator works")

    print("All utility tests passed!")
```

**Step 2: Run tests**

```bash
cd scripts
python3.13 scraper/utils.py
```

Expected: Output "✓ slugify works", "✓ retry decorator works", "All utility tests passed!"

**Step 3: Commit**

```bash
git add scripts/scraper/utils.py
git commit -m "feat: add utility functions for logging and retry logic"
```

---

## Task 4: Romaji Generator

**Files:**
- Modify: `scripts/scraper/utils.py`

**Step 1: Add romaji generation function**

Add to `scripts/scraper/utils.py` after the slugify function:

```python
def generate_romaji(japanese_text: str) -> str:
    """Convert Japanese text to romaji using pykakasi."""
    try:
        import pykakasi
        kks = pykakasi.kakasi()
        result = kks.convert(japanese_text)
        # Join all converted parts with spaces
        romaji_parts = [item['hepburn'] for item in result]
        return ' '.join(romaji_parts)
    except Exception as e:
        logger.error(f"Failed to generate romaji for '{japanese_text}': {e}")
        return japanese_text  # Fallback to original
```

**Step 2: Update test section**

Add to the `if __name__ == '__main__':` section:

```python
    # Test romaji generation
    romaji = generate_romaji("これは本です。")
    print(f"✓ romaji generation works: {romaji}")
    assert "kore" in romaji.lower()
```

**Step 3: Run test**

```bash
cd scripts
python3.13 scraper/utils.py
```

Expected: Output includes "✓ romaji generation works: Kore wa hon desu."

**Step 4: Commit**

```bash
git add scripts/scraper/utils.py
git commit -m "feat: add romaji generation with pykakasi"
```

---

## Task 5: HTTP Fetcher with Rate Limiting

**Files:**
- Modify: `scripts/scraper/utils.py`

**Step 1: Add fetch_url function**

Add to `scripts/scraper/utils.py` after imports:

```python
import requests
from typing import Optional

# Rate limiting
LAST_REQUEST_TIME = 0
MIN_REQUEST_INTERVAL = 1.5  # seconds


@retry(max_attempts=3, delay=2.0, backoff=2.0)
def fetch_url(url: str, delay: float = MIN_REQUEST_INTERVAL) -> Optional[str]:
    """Fetch URL content with rate limiting and retry logic."""
    global LAST_REQUEST_TIME

    # Rate limiting
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < delay:
        sleep_time = delay - elapsed
        logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
        time.sleep(sleep_time)

    logger.info(f"Fetching: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = 'utf-8'

    LAST_REQUEST_TIME = time.time()

    return response.text
```

**Step 2: Test with real request (manual)**

Add to test section:

```python
    # Test fetch_url (manual check - commented out for CI)
    # html = fetch_url("https://jlptsensei.com")
    # assert html is not None
    # print("✓ fetch_url works")
    print("✓ fetch_url defined (manual test required)")
```

**Step 3: Run test**

```bash
cd scripts
python3.13 scraper/utils.py
```

Expected: All tests pass including "✓ fetch_url defined"

**Step 4: Commit**

```bash
git add scripts/scraper/utils.py
git commit -m "feat: add HTTP fetcher with rate limiting"
```

---

## Task 6: HTML Parser for Grammar List Page

**Files:**
- Create: `scripts/scraper/jlpt_sensei_scraper.py`

**Step 1: Write list page parser**

Create `scripts/scraper/jlpt_sensei_scraper.py`:

```python
from bs4 import BeautifulSoup
from typing import List, Dict
from .utils import fetch_url, logger


class JLPTSenseiScraper:
    """Scraper for JLPT Sensei grammar points."""

    BASE_URL = "https://jlptsensei.com"

    LEVEL_URLS = {
        'N5': f"{BASE_URL}/jlpt-n5-grammar-list/",
        'N4': f"{BASE_URL}/jlpt-n4-grammar-list/",
        'N3': f"{BASE_URL}/jlpt-n3-grammar-list/",
        'N2': f"{BASE_URL}/jlpt-n2-grammar-list/",
    }

    def __init__(self, delay: float = 1.5):
        self.delay = delay

    def fetch_grammar_links(self, level: str) -> List[Dict[str, str]]:
        """Fetch all grammar point links from a level's list page."""
        if level not in self.LEVEL_URLS:
            raise ValueError(f"Invalid JLPT level: {level}")

        url = self.LEVEL_URLS[level]
        html = fetch_url(url, delay=self.delay)

        if not html:
            logger.error(f"Failed to fetch {url}")
            return []

        soup = BeautifulSoup(html, 'html.parser')
        grammar_links = []

        # Find grammar links - they typically contain "/learn-japanese-grammar/"
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if '/learn-japanese-grammar/' in href:
                # Get full URL
                if not href.startswith('http'):
                    href = self.BASE_URL + href

                # Extract title from link text
                title = link.get_text(strip=True)

                if title and href not in [g['url'] for g in grammar_links]:
                    grammar_links.append({
                        'title': title,
                        'url': href,
                        'level': level
                    })

        logger.info(f"Found {len(grammar_links)} grammar points for {level}")
        return grammar_links


# Test
if __name__ == '__main__':
    scraper = JLPTSenseiScraper()

    # Test with N5 (smallest set)
    print("Testing N5 grammar list fetch...")
    links = scraper.fetch_grammar_links('N5')

    if links:
        print(f"✓ Found {len(links)} grammar points")
        print(f"  First item: {links[0]['title']} -> {links[0]['url']}")
    else:
        print("✗ No links found (check website structure)")
```

**Step 2: Run test (requires internet)**

```bash
cd scripts
python3.13 -m scraper.jlpt_sensei_scraper
```

Expected: Output shows grammar points found for N5 level

**Step 3: Commit**

```bash
git add scripts/scraper/jlpt_sensei_scraper.py
git commit -m "feat: add grammar list page parser"
```

---

## Task 7: HTML Parser for Grammar Detail Page

**Files:**
- Modify: `scripts/scraper/jlpt_sensei_scraper.py`

**Step 1: Add detail page parser method**

Add to `JLPTSenseiScraper` class:

```python
    def parse_grammar_detail(self, url: str, level: str) -> Optional[Dict]:
        """Parse a grammar detail page and extract all information."""
        from .utils import generate_romaji, slugify

        html = fetch_url(url, delay=self.delay)
        if not html:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        try:
            # Extract title (usually in h1 or specific class)
            title_elem = soup.find('h1')
            if not title_elem:
                logger.warning(f"No title found for {url}")
                return None

            title = title_elem.get_text(strip=True)

            # Extract explanation/meaning section
            # Look for sections with "meaning" or "explanation" in heading
            explanation = ""
            for heading in soup.find_all(['h2', 'h3', 'h4']):
                heading_text = heading.get_text(strip=True).lower()
                if 'meaning' in heading_text or 'explanation' in heading_text:
                    # Get the next paragraph or div
                    next_elem = heading.find_next(['p', 'div'])
                    if next_elem:
                        explanation = next_elem.get_text(strip=True)
                        break

            if not explanation:
                # Fallback: get first paragraph after h1
                first_p = soup.find('h1').find_next('p')
                if first_p:
                    explanation = first_p.get_text(strip=True)

            # Extract examples
            examples = []

            # Look for example sections - common patterns:
            # - <div class="example"> or similar
            # - Japanese text followed by English translation
            example_containers = soup.find_all(['div', 'li'], class_=lambda x: x and 'example' in x.lower() if x else False)

            if not example_containers:
                # Fallback: look for <p> tags with Japanese characters
                example_containers = soup.find_all('p')

            for container in example_containers:
                text = container.get_text('\n', strip=True)
                lines = [line.strip() for line in text.split('\n') if line.strip()]

                # Heuristic: Japanese line followed by English line
                for i in range(len(lines) - 1):
                    japanese_line = lines[i]
                    english_line = lines[i + 1]

                    # Check if first line has Japanese characters
                    if any('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF' or '\u4E00' <= c <= '\u9FFF' for c in japanese_line):
                        examples.append({
                            'japanese': japanese_line,
                            'romaji': generate_romaji(japanese_line),
                            'englishTranslation': english_line
                        })

                        if len(examples) >= 5:  # Limit to 5 examples
                            break

                if len(examples) >= 5:
                    break

            # Create grammar point ID from URL
            grammar_id = url.rstrip('/').split('/')[-1]
            if not grammar_id:
                grammar_id = slugify(title)

            return {
                'id': grammar_id,
                'title': title,
                'titleRomaji': generate_romaji(title),
                'explanationEN': explanation,
                'examples': examples,
                'jlptLevel': level,
                'source': 'JLPT Sensei',
                'url': url
            }

        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
            return None
```

Add import at top:

```python
from typing import List, Dict, Optional
```

**Step 2: Add test**

Update test section:

```python
if __name__ == '__main__':
    scraper = JLPTSenseiScraper()

    # Test with N5 list
    print("Testing N5 grammar list fetch...")
    links = scraper.fetch_grammar_links('N5')

    if links:
        print(f"✓ Found {len(links)} grammar points")

        # Test detail page parsing with first item
        print(f"\nTesting detail page parse: {links[0]['url']}")
        detail = scraper.parse_grammar_detail(links[0]['url'], 'N5')

        if detail:
            print(f"✓ Parsed successfully")
            print(f"  Title: {detail['title']}")
            print(f"  Romaji: {detail['titleRomaji']}")
            print(f"  Explanation: {detail['explanationEN'][:100]}...")
            print(f"  Examples: {len(detail['examples'])}")
        else:
            print("✗ Failed to parse detail page")
    else:
        print("✗ No links found")
```

**Step 3: Run test**

```bash
cd scripts
python3.13 -m scraper.jlpt_sensei_scraper
```

Expected: Shows parsed grammar detail with title, romaji, explanation, and examples

**Step 4: Commit**

```bash
git add scripts/scraper/jlpt_sensei_scraper.py
git commit -m "feat: add grammar detail page parser"
```

---

## Task 8: Main Scraping Method with Progress Tracking

**Files:**
- Modify: `scripts/scraper/jlpt_sensei_scraper.py`

**Step 1: Add main scrape method**

Add to `JLPTSenseiScraper` class:

```python
    def scrape_all(self, levels: List[str] = None) -> List[Dict]:
        """Scrape all grammar points for specified levels."""
        if levels is None:
            levels = ['N5', 'N4', 'N3', 'N2']

        all_grammar = []

        for level in levels:
            logger.info(f"Starting {level} level...")

            # Fetch list page
            links = self.fetch_grammar_links(level)
            if not links:
                logger.warning(f"No links found for {level}")
                continue

            # Parse each detail page
            for i, link_info in enumerate(links, 1):
                logger.info(f"Processing {level} {i}/{len(links)}: {link_info['title']}")

                detail = self.parse_grammar_detail(link_info['url'], level)

                if detail and len(detail.get('examples', [])) >= 2:
                    all_grammar.append(detail)
                    logger.info(f"  ✓ Added: {detail['id']}")
                else:
                    logger.warning(f"  ✗ Skipped (insufficient data): {link_info['url']}")

            logger.info(f"Completed {level}: {len([g for g in all_grammar if g['jlptLevel'] == level])} grammar points")

        logger.info(f"Total grammar points scraped: {len(all_grammar)}")
        return all_grammar
```

**Step 2: Test with single level**

Update test:

```python
if __name__ == '__main__':
    import sys

    scraper = JLPTSenseiScraper(delay=1.0)  # Faster for testing

    # Test scrape just N5
    print("Testing full N5 scrape (first 3 items only)...")

    links = scraper.fetch_grammar_links('N5')
    test_links = links[:3] if len(links) > 3 else links

    results = []
    for link_info in test_links:
        detail = scraper.parse_grammar_detail(link_info['url'], 'N5')
        if detail:
            results.append(detail)

    print(f"\n✓ Successfully scraped {len(results)}/3 test items")

    for item in results:
        print(f"  - {item['id']}: {len(item['examples'])} examples")
```

**Step 3: Run test**

```bash
cd scripts
python3.13 -m scraper.jlpt_sensei_scraper
```

Expected: Successfully scrapes and parses 3 N5 grammar points

**Step 4: Commit**

```bash
git add scripts/scraper/jlpt_sensei_scraper.py
git commit -m "feat: add main scraping method with progress tracking"
```

---

## Task 9: JSON Output with Validation

**Files:**
- Modify: `scripts/scraper/jlpt_sensei_scraper.py`

**Step 1: Add save method**

Add to `JLPTSenseiScraper` class:

```python
    def save_to_json(self, grammar_points: List[Dict], output_path: str) -> None:
        """Save grammar points to JSON file with validation."""
        import json
        from .models import GrammarPoint, Example

        # Validate all grammar points
        validated = []
        for data in grammar_points:
            try:
                # Convert examples to Pydantic models
                examples = [Example(**ex) for ex in data['examples']]

                # Create GrammarPoint model
                grammar = GrammarPoint(
                    id=data['id'],
                    title=data['title'],
                    titleRomaji=data['titleRomaji'],
                    explanationEN=data['explanationEN'],
                    examples=examples,
                    jlptLevel=data['jlptLevel'],
                    source=data.get('source', 'JLPT Sensei'),
                    url=data['url']
                )

                validated.append(grammar.model_dump())

            except Exception as e:
                logger.error(f"Validation failed for {data.get('id', 'unknown')}: {e}")

        logger.info(f"Validated {len(validated)}/{len(grammar_points)} grammar points")

        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(validated, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved to {output_path}")
```

**Step 2: Update test to save JSON**

Update test:

```python
if __name__ == '__main__':
    import json
    import tempfile

    scraper = JLPTSenseiScraper(delay=1.0)

    # Test with 2 items
    links = scraper.fetch_grammar_links('N5')[:2]

    results = []
    for link_info in links:
        detail = scraper.parse_grammar_detail(link_info['url'], 'N5')
        if detail:
            results.append(detail)

    # Test save
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    scraper.save_to_json(results, temp_path)

    # Verify saved file
    with open(temp_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    print(f"✓ Saved {len(saved_data)} items to JSON")
    print(f"✓ First item ID: {saved_data[0]['id']}")

    import os
    os.unlink(temp_path)
```

**Step 3: Run test**

```bash
cd scripts
python3.13 -m scraper.jlpt_sensei_scraper
```

Expected: Successfully validates and saves JSON

**Step 4: Commit**

```bash
git add scripts/scraper/jlpt_sensei_scraper.py
git commit -m "feat: add JSON output with Pydantic validation"
```

---

## Task 10: Command Line Interface

**Files:**
- Create: `scripts/run_scraper.py`

**Step 1: Write CLI script**

Create `scripts/run_scraper.py`:

```python
#!/usr/bin/env python3.13
"""
JLPT Sensei Grammar Scraper CLI

Usage:
    python run_scraper.py --levels N5 N4 --output ../data/grammar_raw.json
"""

import argparse
import sys
import os
from pathlib import Path

# Add scraper to path
sys.path.insert(0, str(Path(__file__).parent))

from scraper.jlpt_sensei_scraper import JLPTSenseiScraper
from scraper.utils import logger


def main():
    parser = argparse.ArgumentParser(
        description='Scrape Japanese grammar points from JLPT Sensei'
    )

    parser.add_argument(
        '--levels',
        nargs='+',
        choices=['N5', 'N4', 'N3', 'N2'],
        default=['N5', 'N4', 'N3', 'N2'],
        help='JLPT levels to scrape (default: all)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='../data/grammar_raw.json',
        help='Output JSON file path (default: ../data/grammar_raw.json)'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.5,
        help='Delay between requests in seconds (default: 1.5)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of grammar points per level (for testing)'
    )

    args = parser.parse_args()

    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting scraper for levels: {', '.join(args.levels)}")
    logger.info(f"Output file: {output_path.absolute()}")
    logger.info(f"Request delay: {args.delay}s")

    # Run scraper
    scraper = JLPTSenseiScraper(delay=args.delay)

    if args.limit:
        # Limited scrape for testing
        logger.info(f"TEST MODE: Limiting to {args.limit} items per level")
        all_grammar = []

        for level in args.levels:
            links = scraper.fetch_grammar_links(level)
            limited_links = links[:args.limit]

            for link_info in limited_links:
                detail = scraper.parse_grammar_detail(link_info['url'], level)
                if detail:
                    all_grammar.append(detail)
    else:
        # Full scrape
        all_grammar = scraper.scrape_all(args.levels)

    # Save results
    scraper.save_to_json(all_grammar, str(output_path))

    # Print summary
    logger.info("=" * 60)
    logger.info("SCRAPING COMPLETE")
    logger.info(f"Total grammar points: {len(all_grammar)}")

    for level in args.levels:
        count = len([g for g in all_grammar if g['jlptLevel'] == level])
        logger.info(f"  {level}: {count} points")

    logger.info(f"Output saved to: {output_path.absolute()}")
    logger.info("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Step 2: Test CLI help**

```bash
cd scripts
python3.13 run_scraper.py --help
```

Expected: Shows help message with all options

**Step 3: Test with limit (2 items from N5)**

```bash
cd scripts
python3.13 run_scraper.py --levels N5 --output /tmp/test_grammar.json --limit 2
```

Expected: Scrapes 2 N5 items and saves to /tmp/test_grammar.json

**Step 4: Verify output**

```bash
cat /tmp/test_grammar.json | python3.13 -m json.tool | head -20
```

Expected: Valid JSON with grammar points

**Step 5: Commit**

```bash
git add scripts/run_scraper.py
chmod +x scripts/run_scraper.py
git commit -m "feat: add command-line interface for scraper"
```

---

## Task 11: Documentation and README

**Files:**
- Create: `scripts/README.md`

**Step 1: Write README**

Create `scripts/README.md`:

```markdown
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
```

**Step 2: Commit**

```bash
git add scripts/README.md
git commit -m "docs: add scraper README with usage instructions"
```

---

## Task 12: Full Integration Test

**Files:**
- Test all components together

**Step 1: Run full N5 scrape (limited)**

```bash
cd scripts
python3.13 run_scraper.py --levels N5 --limit 10 --output ../data/grammar_raw_test.json
```

Expected: Successfully scrapes 10 N5 grammar points

**Step 2: Verify output structure**

```bash
python3.13 -c "
import json
with open('../data/grammar_raw_test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Total items: {len(data)}')
    print(f'First item ID: {data[0][\"id\"]}')
    print(f'First item examples: {len(data[0][\"examples\"])}')
    print(f'All have 2+ examples: {all(len(item[\"examples\"]) >= 2 for item in data)}')
"
```

Expected: All validation checks pass

**Step 3: Clean up test file**

```bash
rm ../data/grammar_raw_test.json
```

**Step 4: Document completion**

Update main design doc with status:

```bash
echo "## Implementation Status

✅ Scraper implemented and tested
- All components working
- Full integration tested with N5 level
- Ready for production scraping

Next: Run full scrape for N5-N2 levels" >> ../docs/plans/2026-01-17-jlpt-sensei-scraper-design.md
```

**Step 5: Final commit**

```bash
git add ../docs/plans/2026-01-17-jlpt-sensei-scraper-design.md
git commit -m "docs: mark scraper implementation as complete"
```

---

## Final Step: Production Scraping

**Files:**
- Execute full scrape

**Step 1: Run full production scrape**

```bash
cd scripts
python3.13 run_scraper.py --levels N5 N4 N3 N2 --output ../data/grammar_raw.json
```

Expected:
- Takes 30-60 minutes depending on request delay
- Outputs 150-180 grammar points
- Saves to `data/grammar_raw.json`

**Step 2: Verify results**

```bash
python3.13 -c "
import json
with open('../data/grammar_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    print('='*60)
    print('SCRAPING RESULTS')
    print('='*60)
    print(f'Total grammar points: {len(data)}')
    print()

    for level in ['N5', 'N4', 'N3', 'N2']:
        count = len([g for g in data if g['jlptLevel'] == level])
        print(f'{level}: {count} points')

    print()
    print('Validation:')
    print(f'  All have IDs: {all(\"id\" in item for item in data)}')
    print(f'  All have 2+ examples: {all(len(item[\"examples\"]) >= 2 for item in data)}')
    print(f'  All have explanations: {all(item[\"explanationEN\"] for item in data)}')
    print('='*60)
"
```

Expected: Summary shows 150-180 grammar points across all levels

**Step 3: Backup and commit**

```bash
# Backup existing grammar.json
cp ../data/grammar.json ../data/grammar_backup.json

# Commit the raw scraped data
git add ../data/grammar_raw.json ../data/grammar_backup.json
git commit -m "feat: add scraped grammar data (150-180 points, English only)"
```

**Step 4: Document next steps**

```bash
echo "
## Next Steps for Translation

1. Review \`data/grammar_raw.json\`
2. Send to Claude for batch translation (English → Chinese)
3. Save translated output as new file
4. Merge into \`data/grammar.json\`

Translation prompt for Claude:
\`\`\`
Please translate this Japanese grammar data from English to Chinese.

For each item:
- Translate 'explanationEN' to Chinese (keep as 'explanation')
- Translate 'englishTranslation' in examples to Chinese (rename to 'english')
- Keep all other fields unchanged (id, title, titleRomaji, japanese, romaji, jlptLevel, source, url)

Output format should match the existing grammar.json structure.
\`\`\`
" >> ../docs/plans/2026-01-17-jlpt-sensei-scraper-design.md
```

**Step 5: Final commit**

```bash
git add ../docs/plans/2026-01-17-jlpt-sensei-scraper-design.md
git commit -m "docs: add translation instructions for scraped data"
```

---

## Success Criteria

- ✅ Scraper runs without errors
- ✅ Outputs valid JSON matching schema
- ✅ Each grammar point has:
  - Unique ID
  - Japanese title with romaji
  - English explanation
  - Minimum 2 example sentences
  - JLPT level metadata
  - Source URL
- ✅ Rate limiting prevents server overload
- ✅ Retry logic handles temporary failures
- ✅ Detailed logging tracks progress
- ✅ 150+ grammar points scraped across N5-N2

## Notes

- The scraper preserves English explanations for manual translation
- Romaji is auto-generated by pykakasi
- HTML parsing may need adjustments if website structure changes
- Test with `--limit` flag before full production scrape
