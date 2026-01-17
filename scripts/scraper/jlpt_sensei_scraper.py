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
