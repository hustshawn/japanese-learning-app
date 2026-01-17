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
    text = re.sub(r'[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', '', text)
    # Replace multiple spaces/whitespace with single hyphen
    text = re.sub(r'\s+', '-', text.strip())
    # Lowercase
    return text.lower()


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

    print("All utility tests passed!")
