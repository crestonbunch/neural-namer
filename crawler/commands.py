"""Main entrypoint for crawler commands."""

import argparse
import crawler.wikia.commands as wikia

def main():
    """Execute the crawler commandline interface."""

    parser = argparse.ArgumentParser(
        description="Crawl data sources for fantasy names.",
    )

    parser.add_argument(
        'source',
        type=str,
        help='Data source to download. Available options: wikia',
    )

    parser.add_argument(
        '--out',
        type=str,
        help='File to store labeled data in'
    )

    args = parser.parse_args()

    if args.source.lower() == 'wikia':
        fetch_func = wikia.fetch
    else:
        raise Exception('Please provide a data source.')

    fetch_func(args.out)
