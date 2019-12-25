from common.util import get_if_char, read_until_chars, get_char_skip_chars, skip_char_til_chars \
    ,read_chars_til_char, Stream
part_of_speech = [
    "noun", "verb", "adjective", "adverb", "determiner",
    "article", "preposition", "conjunction", "proper noun",
    "letter", "character", "phrase", "proverb", "idiom",
    "symbol", "syllable", "numeral", "initialism", "interjection",
    "definitions", "pronoun", "particle", "predicative", "participle",
    "suffix",    
]

def read_a_line(stream):
    while True:
        c = stream.next()
        if c is None:
            break
        if c == '\n':
            yield c
            break
        elif c in ('{', '['):
            token = c + get_if_char(stream, c)
            if token == '{{': 
                skip_char_til_chars(stream, '}')
                stream.next()
                stream.next()
            elif token == '[[':
                yield from read_chars_til_char(stream, '|]')
                skip_char_til_chars(stream, ']')
                stream.next()
                stream.next()
        elif c != "'":
            yield c
    

def parse_list(stream):
    while True:
        chars = list(read_a_line(stream))
        if not chars:
            break
        line = ''.join(chars).strip()
        if line and line[0] == '=':
            break
        elif line and line[0:2] == '# ':
            yield line[2:].strip()

def distinct_list(seq): # Order preserving
  seen = set()
  return [x for x in seq if x not in seen and not seen.add(x)]

def parse_wikitext(text, template_name, template_param, ns):
    stream = Stream(text)
    data = {}
    bol = True
    while True:
        c = stream.next()
        if c is None:
            break
        bol = c in ('\r', '\n')
        if bol:
            c = get_char_skip_chars(stream, ' \r\n')
        if c in ('{', '[') or (c == '=' and bol):
            token = c + get_if_char(stream, c)
            if token == '{{': 
                if template_name not in data:
                    t = read_until_chars(stream, '|}')
                    if t == template_name:
                        stream.next()
                        p = read_until_chars(stream, '|')
                        if p == template_param:
                            stream.next()
                            read_until_chars(stream, '/[')
                            stream.next()
                            data[template_name] = read_until_chars(stream, '/]')
            elif token == '[[':
                if ns not in data:
                    s = read_until_chars(stream, ':]')
                    if s == ns:
                        stream.next()
                        data[ns] = read_until_chars(stream, '|')
            elif c == '=' :
                pos = read_until_chars(stream, '=')
                skip_char_til_chars(stream, '\n')
                stream.next()
                pos = pos.lower()
                if pos in part_of_speech:
                    pos_list = distinct_list(parse_list(stream))
                    if pos_list:
                        if 'pos' not in data:
                            data['pos'] = {}
                        if pos not in data['pos']:
                            data['pos'][pos] = pos_list
    return data