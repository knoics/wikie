import time
from collections import defaultdict
import json

from word_extractor.wikie import pronunciation_to_numbers, get_wiktionary_pages, parse_words
from xml_parser.simple_xml_parser import xml_to_dict

def parse_wiktionary(file_path, max_count=None):
    count = 1
    for word, pronunciation, image_file in parse_words(file_path):
        if ',' not in word and ',' in pronunciation:
            pronunciation = pronunciation.split(',')[0]
        numbers = pronunciation_to_numbers(pronunciation)
        yield (count, word, pronunciation, numbers, image_file)
        count += 1
        if max_count and count > max_count:
            break

def extract_words(wiktionary_file, word_number_file):
    start_time = time.time()
    with open(word_number_file, "w") as text_file:
        for count, word, pronunciation, numbers, _ in parse_wiktionary(wiktionary_file):
            text_file.write("%s|%s|%s|%s\n" % (count, word, pronunciation, numbers))
    print('done!, took %s seconds.' % (time.time() - start_time))

def convert_to_number(word_file):
    numbers = defaultdict(list)
    with open(word_file, "r") as text_file:
        while True:
            line = text_file.readline()
            if not line:
                break
            d = json.loads(line)
            word = d['title']
            number = d['ms']
            if not number:
                continue
            numbers[number].append(word)
    return numbers   

def write_number_to_file(numbers, number_file):
    count = 0
    with open(number_file, "w") as text_file:
        for number, words in numbers.items():
            d = {'ms': number, 'words': words}
            text_file.write(json.dumps(d, ensure_ascii=False) + '\n')
            count += 1
    print('numbers written: ', count) 
    
def filter_subset(wiktionary_file, filter, result_file, limits=None):
    filtered_count = 0
    with open(result_file, "w") as text_file:
        for count, page in get_wiktionary_pages(wiktionary_file):
            if filter(page):
                text_file.write(page)
                filtered_count += 1
                if limits and filtered_count >= limits:
                    break
            if count % 10000 == 0:
                print('scanned pages: ', count, filtered_count, int(filtered_count*100/count))

def transform(wiktionary_file, map, result_file, limits=None):
    with open(result_file, "w") as text_file:
        for count, page in get_wiktionary_pages(wiktionary_file):
            text_file.write(map(page))
            if limits and count >= limits:
                break
            if count % 10000 == 0:
                print('transformed pages: ', count)

def filter(source_file, filter, result_file, limits=0):
    count = 1
    filtered_count = 0
    with open(result_file, "w") as text_file:
        with open(source_file, "r") as src_file:
            for line in src_file.readlines():
                if filter(line):
                    text_file.write(line)
                else:
                    filtered_count += 1
                    print('filtered ', filtered_count, line)
                if limits and count >= limits:
                    break
                if count % 10000 == 0:
                    print('transformed pages: ', count)
                count += 1
            print('done with transform: ', count, filtered_count)
            
def transform_word_file_to_number_file(word_file, number_file):
    write_number_to_file(convert_to_number(word_file), number_file)

# with open(r'./number_words.txt', "r") as text_file:
#     while True:
#         line = text_file.readline()
#         if not line:
#             break
#         number_words = line.split('||')
#         assert len(number_words) == 2, 'format not correct ! %s' % line

# print('verified')
