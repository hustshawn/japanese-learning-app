import logging
import time
from functools import wraps
from typing import Callable, Any
import requests
from typing import Optional

# Rate limiting
LAST_REQUEST_TIME = 0
MIN_REQUEST_INTERVAL = 1.5  # seconds

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
    text = re.sub(r'[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', '', text)
    # Replace multiple spaces/whitespace with single hyphen
    text = re.sub(r'\s+', '-', text.strip())
    # Lowercase
    return text.lower()


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


# Test utilities
if __name__ == '__main__':
    # Test slugify
    assert slugify("は (wa) - Topic Marker") == "は-wa-topic-marker"
    print("✓ slugify works")

    # Test retry
    def test_retry():
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

    test_retry()

    # Test romaji generation
    romaji = generate_romaji("これは本です。")
    print(f"✓ romaji generation works: {romaji}")
    assert "kore" in romaji.lower()

    # Test fetch_url (manual check - commented out for CI)
    # html = fetch_url("https://jlptsensei.com")
    # assert html is not None
    # print("✓ fetch_url works")
    print("✓ fetch_url defined (manual test required)")

    print("All utility tests passed!")
