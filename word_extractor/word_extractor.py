import time
from collections import defaultdict

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

def convert_number_to_words(word_number_file):
    numbers = defaultdict(list)
    with open(word_number_file, "r") as text_file:
        while True:
            line = text_file.readline()
            if not line:
                break
            items = line.split('|')
            word = items[1]
            number = items[3].strip()
            if not number:
                continue
            numbers[number].append(word)
    return numbers   

def write_number_to_words(numbers, number_word_file):
    with open(number_word_file, "w") as text_file:
        for number, words in numbers.items():
            text_file.write("%s||%s\n" % (number, '|'.join(words))) 
    
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

#extract_words(r'./enwiktionary-latest-pages-articles.xml.bz2', r'./words.txt')
# for count, word, pronunciation, numbers, image_file in parse_wiktionary_with_addinfo(r'./enwiktionary-latest-pages-articles.xml.bz2'):
#     print(count, word, pronunciation, numbers, image_file)
#     if count>=1:
#         break

    
#write_number_to_words(convert_number_to_words(r'./word_numbers.txt'), r'./number_words.txt')

# with open(r'./number_words.txt', "r") as text_file:
#     while True:
#         line = text_file.readline()
#         if not line:
#             break
#         number_words = line.split('||')
#         assert len(number_words) == 2, 'format not correct ! %s' % line

# print('verified')
