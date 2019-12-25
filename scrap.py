from word_extractor.word_extractor import get_wiktionary_pages, filter_subset, transform, transform_word_file_to_number_file
from word_extractor.wikie import parse_page, parse_wiki_page, us_ipa_pattern, ipa_pattern
from common.util import Stream
import re
import json
import cProfile

import time
start = time.time()

def profile():
    # filter_subset(r'./enwiktionary-latest-pages-articles.xml.bz2', lambda page: ipa_pattern.search(page),
    #     r'./enwiktionary-latest-pages-articles.xml.ipa.txt')
    transform(r'./enwiktionary-latest-pages-articles.xml.ipa.txt', lambda page: json.dumps(parse_wiki_page(page), ensure_ascii=False) + '\n', 
    r'./words.json')
    transform_word_file_to_number_file('./words.json', './numbers.json')


#p = re.compile('{{a\|US}}.*?{{(?P<ipa>.*?)}}', re.DOTALL)
#cProfile.run('profile()', 'profile_stats')
profile()

print('took ', time.time() - start)
