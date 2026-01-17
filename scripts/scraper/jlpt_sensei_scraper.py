from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .utils import fetch_url, logger
import json
from .models import GrammarPoint, Example


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
        seen_urls = set()  # For O(1) deduplication

        # Find grammar links - they typically contain "/learn-japanese-grammar/"
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if '/learn-japanese-grammar/' in href:
                # Get full URL with proper path joining
                if not href.startswith('http'):
                    href = self.BASE_URL.rstrip('/') + '/' + href.lstrip('/')

                # Extract title from link text
                title = link.get_text(strip=True)

                if title and href not in seen_urls:
                    grammar_links.append({
                        'title': title,
                        'url': href,
                        'level': level
                    })
                    seen_urls.add(href)

        logger.info(f"Found {len(grammar_links)} grammar points for {level}")
        return grammar_links

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

            # Validate explanation is not empty
            if not explanation:
                logger.warning(f"No explanation found for {url}")
                return None

            # Extract examples
            examples = []

            # JLPT Sensei uses <div class="example-cont"> for each example
            # Each contains:
            # - Japanese: <div class="example-main"><p class="m-0 jp">
            # - Romaji: <div class="example_romaji"><div class="alert alert-info">
            # - English: <div class="example_en"><div class="alert alert-primary">
            example_containers = soup.find_all('div', class_='example-cont')

            for container in example_containers:
                # Extract Japanese sentence
                japanese_elem = container.find('div', class_='example-main')
                if japanese_elem:
                    japanese_p = japanese_elem.find('p', class_='jp')
                    if japanese_p:
                        japanese = japanese_p.get_text(strip=True)
                    else:
                        continue
                else:
                    continue

                # Extract romaji
                romaji_elem = container.find('div', class_='example_romaji')
                if romaji_elem:
                    romaji_alert = romaji_elem.find('div', class_='alert')
                    if romaji_alert:
                        romaji = romaji_alert.get_text(strip=True)
                    else:
                        romaji = generate_romaji(japanese)
                else:
                    romaji = generate_romaji(japanese)

                # Extract English translation
                english_elem = container.find('div', class_='example_en')
                if english_elem:
                    english_alert = english_elem.find('div', class_='alert')
                    if english_alert:
                        english = english_alert.get_text(strip=True)
                    else:
                        continue
                else:
                    continue

                # Add example if we have all three components
                if japanese and romaji and english:
                    examples.append({
                        'japanese': japanese,
                        'romaji': romaji,
                        'englishTranslation': english
                    })

                    if len(examples) >= 5:  # Limit to 5 examples
                        break

            # Validate minimum examples
            if len(examples) < 2:
                logger.warning(f"Insufficient examples ({len(examples)}) for {url}")
                return None

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

    def save_to_json(self, grammar_points: List[Dict], output_path: str) -> None:
        """Save grammar points to JSON file with validation."""
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

                validated.append(grammar.model_dump(mode='json'))

            except Exception as e:
                logger.error(f"Validation failed for {data.get('id', 'unknown')}: {e}")

        logger.info(f"Validated {len(validated)}/{len(grammar_points)} grammar points")

        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(validated, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved to {output_path}")


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
