# Challenge 03: Generator Pipeline

def split_words(text):
    pass  # TODO: yield individual words

def filter_short(words, min_len=4):
    pass  # TODO: yield words with len >= min_len

def upper(words):
    pass  # TODO: yield uppercased words

def pipeline(text):
    # TODO: chain the three generators
    pass

# Test
if __name__ == "__main__":
    result = list(pipeline("hello world foo bar baz python"))
    print(result)  # ["HELLO", "WORLD", "PYTHON"]