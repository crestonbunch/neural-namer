"""Functions to vectorize strings into integers and map between them."""

import pickle
import numpy as np

def vectorize_file(infile, lookupfile, outfile):
    """Convert a data file into vectors and save it to the output."""

    outsamples = []
    outauthors = []
    with open(infile, 'rb') as file_handle:
        samples = pickle.load(file_handle)
        labels = [x['author'] for x in samples]
        inputs = [x['name'] for x in samples]
        max_len = max([len(x) for x in inputs])

        input_map, reverse_input_map = build_input_map(inputs)
        label_map, reverse_label_map = build_label_map(labels)

        for sample in samples:
            author = sample['author']
            pad = [0] * (max_len - len(sample['name']))
            name = [''] + list(sample['name']) + ['']
            vec = [input_map[c] for c in name] + pad
            outsamples.append(vec)
            outauthors.append(label_map[author])

    # shuffle lists
    ind = np.random.permutation(len(outsamples))
    outsamples = np.asarray(outsamples)[ind].tolist()
    outauthors = np.asarray(outauthors)[ind].tolist()

    with open(outfile, 'wb') as file_handle:
        pickle.dump((outsamples, outauthors), file_handle)

    with open(lookupfile, 'wb') as file_handle:
        pickle.dump((input_map, reverse_input_map,
                     label_map, reverse_label_map),
                    file_handle)

def map_str(lookup, string):
    """Convert a string to integers with the given lookup."""
    return [lookup[c] for c in string]

def map_vec(lookup, vec):
    """Convert a vector to a string with the given lookup."""
    return ''.join([lookup[i] for i in vec])

def build_input_map(strings):
    """Build a lookup and reverse lookup from characters to integers."""
    chars = set([''])
    for string in strings:
        chars = chars.union(set(string))

    chars = list(chars)

    lookup = {c: i for (i, c) in enumerate(chars, 1)}
    reverse_lookup = {i: c for (i, c) in enumerate(chars, 1)}

    return lookup, reverse_lookup

def build_label_map(labels):
    labels = set(labels)
    lookup = {l: i for (i, l) in enumerate(labels)}
    reverse_lookup = {i: l for (i, l) in enumerate(labels)}

    return lookup, reverse_lookup
