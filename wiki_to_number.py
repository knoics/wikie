import time

from wikie import parse_word_and_pronunciations, pronunciation_to_numbers

def wiktionary_to_number(file_path, max_count=None):
    count = 1
    for word, pronunciation in parse_word_and_pronunciations(file_path):
        numbers = pronunciation_to_numbers(pronunciation)
        yield (count, word, pronunciation, numbers)
        count += 1
        if max_count and count > max_count:
            break
        
start_time = time.time()
with open("./word_numbers.txt", "w") as text_file:
    for count, word, pronunciation, numbers in wiktionary_to_number(r'./enwiktionary-latest-pages-articles.xml.bz2'):
        if ',' not in word and ',' in pronunciation:
            pronunciation = pronunciation.split(',')[0]
        text_file.write("%s|%s|%s|%s\n" % (count, word, pronunciation, numbers))
print('done!, took %s seconds.' % (time.time() - start_time))