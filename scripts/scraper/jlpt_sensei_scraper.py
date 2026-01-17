from bs4 import BeautifulSoup
from typing import List, Dict, Optional
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
