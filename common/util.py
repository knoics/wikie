def get_char(string):
    for c in string:
        yield c

class Stream():
  def __init__(self, generator):
    self.generator = generator
    self.next_item = next(self.generator, None)

  def next(self):
    next_item = self.next_item
    self.next_item = next(self.generator, None)
    return next_item

  def peek(self):
    return self.next_item

def read_chars_til_char(stream, chars):
    while True:
        if stream.peek() is None:
            break
        if stream.peek() in chars:
            break
        yield stream.next()

def _read_if_char(stream, char):
    while True:
        if char != stream.peek():
            break
        next_char = stream.next()
        if next_char is None:
            break
        yield next_char

def read_until_chars(stream, chars):
    return ''.join(read_chars_til_char(stream, chars))

def get_if_char(stream, char):
    return ''.join(_read_if_char(stream, char))

def get_char_skip_chars(stream, chars_to_skip):
    while True:
        next_char = stream.next()
        if not next_char:
            return None
        if next_char in chars_to_skip:
            continue
        return next_char

def skip_char_til_chars(stream, chars):
    while True:
        if stream.peek() is None:
            break
        if stream.peek() in chars:
            break
        next_char = stream.next()
        if not next_char:
            break
