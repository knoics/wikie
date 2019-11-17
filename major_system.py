consonant_to_number_map = {
    's' : '0',
    'z' : '0',
    't' : '1',
    'd' : '1',
    'n' : '2',
    'm' : '3',
    'ɹ' : '4',
    'l' : '5',
    'j' : '6',
    't͡ʃ': '6',
    'dʒ': '6',
    'ʒ' : '6',
    'ʃ' : '6',
    'k' : '7',
    'g' : '7',
    'ɡ' : '7',
    'f' : '8',
    'v' : '8',
    'b' : '9',
    'p' : '9'
}
consonants = set(consonant_to_number_map.keys())
def find_consonant(pronunciation, i):
    for l in range(3,0,-1):
        if pronunciation[i:i+l] in consonants:
            return pronunciation[i:i+l]
    return ''

def pronunciation_to_consonants(pronunciation):
    i = 0
    size = len(pronunciation)
    while i<size:
        c = find_consonant(pronunciation, i)
        if c:
            yield c
            i += len(c)
        else:
            i += 1

def pronunciation_to_numbers(pronunciation):
    return ''.join([consonant_to_number_map[c] for c in pronunciation_to_consonants(pronunciation)])

print(pronunciation_to_numbers('ɡɹiːs'))