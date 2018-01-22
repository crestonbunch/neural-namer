"""Main entrypoint for modeler commands."""

import argparse

from modeler.train import train
from modeler.gen import gen

def main():
    """Execute the modeler commandline interface."""

    parser = argparse.ArgumentParser(
        description="Train and run the music generator.""",
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    train_parser = subparsers.add_parser(
        'train', help='Train a model'
    )
    train_parser.add_argument('--datafile', type=str, help='Data file to sample from')
    train_parser.add_argument('--savedir', type=str, help='Directory to store model in')
    train_parser.add_argument('--embed_size', default=32, type=int, help='Size of character embedding')
    train_parser.add_argument('--ctx_size', default=8, type=int, help='Size of author embedding')
    train_parser.add_argument('--input_dropout', default=0.5, type=float, help='Rate of input dropout')
    train_parser.add_argument('--output_dropout', default=0.5, type=float, help='Rate of output dropout')
    train_parser.add_argument('--cell', default='lstm', choices=['lstm', 'gru', 'rnn'], help='Cell type')
    train_parser.add_argument('--cell_size', default=128, type=int, help='Number of hidden nodes in each cell')
    train_parser.add_argument('--cell_num', default=1, type=int, help='Number of RNN cells')
    train_parser.add_argument('--activation', default='relu', choices=['relu','tanh','sigmoid'], help='Activation func')
    train_parser.add_argument('--num_gpu', default=2, type=int, help='Number of GPU devices to compute with')
    train_parser.add_argument('--optimizer', default='Adam', choices=['Adam', 'SGD'], help='Optimizer to use')
    train_parser.add_argument('--learn_rate', default=0.001, type=float, help='Learn rate of the model')
    train_parser.add_argument('--decay_rate', default=0.95, type=float, help='Decay of the learning rate')
    train_parser.add_argument('--decay_steps', default=100, type=int, help='Decay the learning rate every x steps')
    train_parser.add_argument('--grad_clip', default=0.5, type=float, help='Clipping value for global gradient norm')
    train_parser.add_argument('--num_epochs', default=100, type=int, help='Number of epochs')
    train_parser.add_argument('--batch_size', default=128, type=int, help='Samples per batch')
    train_parser.set_defaults(learning=True)

    gen_parser = subparsers.add_parser(
        'gen', help='Generate samples'
    )
    gen_parser.add_argument('--datafile', type=str, help='Data file from the preprocessing step')
    gen_parser.add_argument('--lookupfile', type=str, help='File that stores the lookup maps')
    gen_parser.add_argument('--savedir', type=str, help='Stored model directory from the training step')
    gen_parser.add_argument(
        '--author', type=str, default='Tolkien', help='Author to emulate. Options are: ' + \
        '"Tolkien", "George Martin", "Robert Jordan", "Steven Erikson", ' + \
        '"Brian Jacques", "Frank Herbert"'
    )
    gen_parser.add_argument('--num', default=20, type=int, help='Number of names to generate')
    gen_parser.set_defaults(learning=False)

    args = parser.parse_args()

    if args.learning:
        train(args.savedir, args)
    else:
        print('\n'.join(
            gen(args.savedir, args.lookupfile, args.datafile, args.author, args.num))
        )
