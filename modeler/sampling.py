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
            yield _pad_batch(seqs), _pad_batch(targets), _pad_batch(auths)
            seqs, targets, auths = [], [], []

    yield _pad_batch(seqs), _pad_batch(targets), _pad_batch(auths)

def _pad_batch(batch):
    max_len = max([len(x) for x in batch])
    return [x + [0]*(max_len - len(x)) for x in batch]