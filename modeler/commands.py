"""Main entrypoint for modeler commands."""

import argparse

from modeler.train import train
from modeler.gen import gen

def main():
    """Execute the crawler commandline interface."""

    parser = argparse.ArgumentParser(
        description="Train and run the name generator.""",
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    train_parser = subparsers.add_parser(
        'train', help='Train a model'
    )
    train_parser.add_argument('--infile', type=str, help='Data file to sample from')
    train_parser.add_argument('--logdir', type=str, help='File to store logs in')
    train_parser.set_defaults(action='train')

    gen_parser = subparsers.add_parser(
        'gen', help='Generate a name'
    )
    gen_parser.add_argument('--infile', type=str, help='Data file to sample from')
    gen_parser.add_argument('--logdir', type=str, help='File to store logs in')
    gen_parser.add_argument('--lookupfile', type=str, help='Lookup from the preprocessor')
    gen_parser.add_argument('--num', type=int, default=20, help='Number of names to generate')
    gen_parser.add_argument(
        '--author', type=str, default='Tolkein', help='Author to emulate. Options are: ' + \
        '"Tolkien", "George Martin", "Robert Jordan", "Steven Erikson", ' + \
        '"Brian Jacques", "Frank Herbert"'
    )
    gen_parser.set_defaults(action='gen')

    args = parser.parse_args()

    if args.action == 'train':
        train(args.infile, args.logdir)

    if args.action == 'gen':
        gen(args.infile, args.logdir, args.lookupfile, args.author, args.num)
