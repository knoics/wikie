import time
from collections import defaultdict

from wikie import parse_word_and_pronunciations, pronunciation_to_numbers

def wiktionary_to_number(file_path, max_count=None):
    count = 1
    for word, pronunciation in parse_word_and_pronunciations(file_path):
        if ',' not in word and ',' in pronunciation:
            pronunciation = pronunciation.split(',')[0]
        numbers = pronunciation_to_numbers(pronunciation)
        yield (count, word, pronunciation, numbers)
        count += 1
        if max_count and count > max_count:
            break

def extract_word_numbers(wiktionary_file, word_number_file):
    start_time = time.time()
    with open(word_number_file, "w") as text_file:
        for count, word, pronunciation, numbers in wiktionary_to_number(wiktionary_file):
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
    
#extract_word_numbers(r'./enwiktionary-latest-pages-articles.xml.bz2', r'./word_numbers.txt')
write_number_to_words(convert_number_to_words(r'./word_numbers.txt'), r'./number_words.txt')

with open(r'./number_words.txt', "r") as text_file:
    while True:
        line = text_file.readline()
        if not line:
            break
        number_words = line.split('||')
        assert len(number_words) == 2, 'format not correct ! %s' % line

print('verified')