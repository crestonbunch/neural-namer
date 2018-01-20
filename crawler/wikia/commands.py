"""Commands for scraping wikia data for fantasy names."""

import re
import os
import os.path
import pickle
import csv
import urllib.request
import tempfile
from pyunpack import Archive
from lxml import etree
from lxml.etree import XMLParser
from collections import Counter

from crawler.wikia.sources import SOURCES

def fetch(outfile):
    """Fetch character names from sources and save them to the outfile."""
    authors = Counter()
    vocab = Counter()

    parser = XMLParser(huge_tree=True)
    with open(outfile, 'w') as file_handler:
        writer = csv.writer(file_handler)
        for source in SOURCES:
            print('Parsing {}'.format(source['author']))
            doc = download_archive(source['dump_url'])
            names = parse(
                etree.XML(doc, parser=parser), 
                source['root'],
                source['xpath'],
                source['where'],
                source['ignore'],
                source['strip']
            )
            for n in names:
                writer.writerow([n, source['author']])
                authors[source['author']] += 1
                vocab.update(n)

    vocab_list, counts = zip(*vocab.most_common())
    vocab_order = ['', '▶', '◀'] + list(vocab_list)
    vocab_map = {char: i for i, char in enumerate(vocab_order)}
    vocab_freq = [0, 0, 0] + [counts[i] / sum(counts) for i in range(len(vocab_list))]
    author_list, counts = zip(*authors.most_common())
    author_order = list(author_list)
    author_map = {author: i for i, author in enumerate(author_order)}
    with open('{}.meta'.format(outfile), 'wb') as file_handler:
        pickle.dump((vocab_map, vocab_freq, author_map), file_handler)

    print('Wiki counts:')
    print('Vocab size', len(vocab_map))
    print(authors)

def parse(tree, root, xpath, where, ignore, strip):
    """A generator for parsing a wikia data tree."""
    ns = {'n': tree.nsmap[None]}
    root = tree.xpath(root, namespaces=ns)
    for node in root:
        search_contents = node.xpath(where['xpath'], namespaces=ns, smart_strings=False)
        if search_contents and re.search(where['contains'], search_contents[0]):
            title = node.xpath(xpath, namespaces=ns, smart_strings=False)[0]
            blacklist = [re.search(x, title) for x in ignore]
            if not any(blacklist):
                for suffix in strip:
                    title = re.sub(suffix, '', title)
                yield title

def download_archive(url):
    """Download a .7z Mediawiki data dump to a temporary folder."""

    with tempfile.NamedTemporaryFile('wb') as file_handler:
        urllib.request.urlretrieve(url, file_handler.name)
        with tempfile.TemporaryDirectory() as extract_dir:
            Archive(file_handler.name).extractall(extract_dir)
            for filename in os.listdir(extract_dir):
                with open(os.path.join(extract_dir, filename), 'r') as extract_file:
                    return extract_file.read()
