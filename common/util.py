class Stream():
  def __init__(self, items):
    self.items = items
    self.len = len(items)
    self.index = 0

  def next(self):
    if self.index >= self.len:
        return None
    item = self.items[self.index]
    self.index += 1
    return item

  def peek(self):
    if self.index >= self.len:
        return None
    return self.items[self.index]

  def read_line(self):
    peek = self.index
    while peek < self.len and self.items[peek] != '\n':
        peek += 1
    result = self.items[self.index:peek+1]
    self.index = peek + 1
    return result

  def read_lines(self):
    while True:
        line = self.read_line()
        if not line:
            break
        yield line
    
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
