import bz2
import re
from major_system import pronunciation_to_numbers

def get_wiktionary_pages(file_path):
    page_content = ''
    with bz2.open(file_path) as f:
        while True:
            line = f.readline().decode("utf-8") 
            if not line:
                break
            if '<page>' in line:
                page_content += line
            elif page_content:
                page_content += line
            if '</page>' in line:
                yield page_content
                page_content = ''

def parse_word_and_pronunciations(file_path):
    for page in get_wiktionary_pages(file_path):
        match = re.search('<title>(?P<title>.*)</title>.*IPA\|en\|/(?P<ipa_en>.*?)/', page, re.DOTALL)
        if not match:
            continue
        match = match.groupdict()
        title = match.get('title')
        pronunciation = match.get('ipa_en', '')
        if title.startswith('Appendix:'):
            continue
        yield title, pronunciation
