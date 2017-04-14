import numpy as np

def batch_samples(samples, authors, batch_size):
    """Group samples in batches and return tuples sequence, targets"""
    seqs, targets, auths = [], [], []
    for sample, auth in zip(samples, authors):
        seq, target = sample[:-1], sample[1:]
        seqs.append(seq)
        targets.append(target)
        auths.append([auth] * len(seq))
        if len(seqs) >= batch_size:
            yield seqs, targets, auths
            seqs, targets, auths = [], [], []

    yield seqs, targets, auths
