from word_extractor.word_extractor import get_wiktionary_pages, filter_subset
from word_extractor.wikie import parse_page
import cProfile


def profile():
    filter_subset(r'./enwiktionary-latest-pages-articles.xml.bz2', lambda page: '{{IPA' in page,
        r'./enwiktionary-latest-pages-articles.xml.ipa.txt')
        # d = parse_page(page)
        # if d['text']:
        #     print(count, d)

# for count, page in get_wiktionary_pages(r'./enwiktionary-latest-pages-articles.xml.ipa.txt'):
#     if count % 10000 == 0:
#         print(count)
# cProfile.run('profile()', 'profile_stats')
