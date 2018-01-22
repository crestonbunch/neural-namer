"""
This script copies variables from the python model to the JavaScript model to
enable generating names from the web interface.
"""

import os
import argparse
import pickle
import json
from dump_checkpoint_vars import get_checkpoint_dumper

VARIABLES_DIR = os.path.join('web', 'src', 'vars')

AUTHOR_MAP_FILE = os.path.join('web', 'src', 'vars', 'author_map.json')
INDEX_MAP_FILE = os.path.join('web', 'src', 'vars', 'index_map.json')
VOCAB_MAP_FILE = os.path.join('web', 'src', 'vars', 'vocab_map.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--checkpoint_file',
        type=str,
        required=True,
        help='Path to the model checkpoint')
    parser.add_argument(
        '--data_file',
        type=str,
        required=True,
        help='Path to the data csv')

    FLAGS, unparsed = parser.parse_known_args()

    if unparsed:
        parser.print_help()
        print('Unrecognized flags: ', unparsed)
        exit(-1)

    checkpoint_dumper = get_checkpoint_dumper(
        'tensorflow',
        FLAGS.checkpoint_file,
        VARIABLES_DIR,
        "^Optimize"
    )

    checkpoint_dumper.build_and_dump_vars()

    with open('{}.meta'.format(FLAGS.data_file), 'rb') as fh:
        vocab_map, _, author_map = pickle.load(fh)

        with open(VOCAB_MAP_FILE, 'w') as fh:
            json.dump(vocab_map, fh)

        with open(INDEX_MAP_FILE, 'w') as fh:
            json.dump({i: char for char, i in vocab_map.items()}, fh)

        with open(AUTHOR_MAP_FILE, 'w') as fh:
            json.dump(author_map, fh)
