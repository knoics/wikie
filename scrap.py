from word_extractor.word_extractor import get_wiktionary_pages, filter_subset, transform, transform_word_file_to_number_file, filter
from word_extractor.wikie import parse_page, parse_wiki_page, us_ipa_pattern, ipa_pattern
from common.util import Stream
import re
import json
import cProfile

import os
import time
start = time.time()

def profile():
    # filter_subset(r'./enwiktionary-latest-pages-articles.xml.bz2', lambda page: ipa_pattern.search(page),
    #     r'./enwiktionary-latest-pages-articles.xml.ipa.txt')
    transform(r'./enwiktionary-latest-pages-articles.xml.ipa.txt', 
        lambda page: json.dumps(parse_wiki_page(page), ensure_ascii=False) + '\n', 
        r'./words1.json')
    def filter_func(line):
        d = json.loads(line)
        return ':' not in d['title'] and '/' not in d['title']
    filter(r'./words1.json', filter_func, r'./words.json')
    os.remove(r'./words1.json')
    transform_word_file_to_number_file('./words.json', './numbers.json')

# profile()
# with open(r'./words.json', "r") as file:
#     for line in file.readlines():
#         d = json.loads(line)
#         # validation

print('took ', time.time() - start)
