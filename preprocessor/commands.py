"""Main entrypoint for preprocessor commands."""

import argparse
import crawler.wikia.commands as wikia

from preprocessor import vectorizer

def main():
    """Execute the crawler commandline interface."""

    parser = argparse.ArgumentParser(
        description="Preprocess a data file for input into the classifier.",
    )

    parser.add_argument(
        '--infile',
        type=str,
        help='Data file made by the crawler',
    )

    parser.add_argument(
        '--outfile',
        type=str,
        help='File to store preprocessed data in'
    )

    parser.add_argument(
        '--lookupfile',
        type=str,
        help='File to store the character lookup and reverse lookup in'
    )

    args = parser.parse_args()

    vectorizer.vectorize_file(args.infile, args.lookupfile, args.outfile)
