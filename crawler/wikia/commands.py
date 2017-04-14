"""Commands for scraping wikia data for fantasy names."""

import re
import os
import os.path
import pickle
import urllib.request
import tempfile
from pyunpack import Archive
from lxml import etree
from lxml.etree import XMLParser
from collections import defaultdict

from crawler.wikia.sources import SOURCES

def fetch(outfile):
    """Fetch character names from sources and save them to the outfile."""
    data = []
    counts = defaultdict(int)

    parser = XMLParser(huge_tree=True)
    for source in SOURCES:
        doc = download_archive(source['dump_url'])
        names = list(parse(
            etree.XML(doc, parser=parser), 
            source['root'], source['xpath'], source['where'], source['ignore'],
        ))
        data.extend([{'name': n, 'author': source['author']} for n in names])
        counts[source['author']] += len(names)

    with open(outfile, 'wb') as file_handler:
        pickle.dump(data, file_handler)

    print('Wiki counts:')
    print(counts)

def parse(tree, root, xpath, where, ignore):
    """A generator for parsing a wikia data tree."""
    ns = {'n': tree.nsmap[None]}
    root = tree.xpath(root, namespaces=ns)
    for node in root:
        search_contents = node.xpath(where['xpath'], namespaces=ns, smart_strings=False)
        if search_contents and re.search(where['contains'], search_contents[0]):
            title = node.xpath(xpath, namespaces=ns, smart_strings=False)[0]
            blacklist = [re.search(x, title) for x in ignore]
            if not any(blacklist):
                print(title)
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
