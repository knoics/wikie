import bz2
import re
import os
from major_system.major_system import pronunciation_to_numbers
from xml_parser.simple_xml_parser import xml_to_dict
from wikitext_parser.wikitext_parser import parse_wikitext

def get_wiktionary_pages(file_path):
    page_content = ''
    count = 1
    _, ext_name = os.path.splitext(file_path)
    is_bz2 = ext_name == '.bz2'
    file_open = bz2.open if is_bz2 else open
    with file_open(file_path) as f:
        while True:
            line = f.readline()
            if is_bz2:
                line = line.decode("utf-8") 
            if not line:
                break
            if '<page>' in line:
                page_content += line
            elif page_content:
                page_content += line
            if '</page>' in line:
                yield count, page_content
                count += 1
                page_content = ''

def parse_words(file_path):
    for page in get_wiktionary_pages(file_path):
        match = re.search('<title>(?P<title>.*)</title>.*IPA\|en\|/(?P<ipa_en>.*?)/.*', page, re.DOTALL)
        if not match:
            continue
        match = match.groupdict()
        title = match.get('title')
        pronunciation = match.get('ipa_en', '')
        #image = match.get('image', '')
        image = ''
        if title.startswith('Appendix:'):
            continue
        yield title, pronunciation, image

def parse_page(page):
    d = xml_to_dict(page)['page']
    if not d['revision']['text']:
        text_d = {}
    else:
        text_d = parse_wikitext(d['revision']['text'], 'IPA', 'en', 'File')
    ms = ''
    if 'IPA' in text_d:
        ms = pronunciation_to_numbers(text_d['IPA'])
        text_d['ms'] = ms
    return {
        'title': d['title'],
        'text' : text_d
    }