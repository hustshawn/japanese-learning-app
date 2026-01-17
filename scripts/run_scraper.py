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
