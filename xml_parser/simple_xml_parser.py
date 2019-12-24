from common.util import read_until_chars, get_char, Stream

def parse_xml_to_dict(stream):
    token = ''
    token_value = []
    keys = []
    is_open_braket = False
    while True:
        next_char = stream.next()
        if next_char is None:
            break
        if next_char == '<':
            key = read_until_chars(stream, '>')
            stream.next()
            if key[0] == '/' or key[-1] == '/':
                # end braket
                if key[-1] == '/':
                    k = key[0:-1].strip()
                    k = k.split(' ')[0]
                    data = {k: ''}
                else:
                    k, data = keys.pop()
                    v = ''.join(token_value).strip()
                    if is_open_braket:
                        data[k] = v
                if keys:
                    pk, pdata = keys[-1]
                    pdata[pk].update(data)
                is_open_braket = False
            else:
                # start braket
                key = key.split(' ')[0]
                keys.append((key, {key: {}}))
                is_open_braket = True
            token_value = []
            continue
        else:
            token_value.append(next_char)

    return data

def xml_to_dict(xml):
    stream = Stream(get_char(xml))
    return parse_xml_to_dict(stream)