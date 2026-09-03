# Generator pipeline
def read_lines(text):
    for line in text.split(chr(10)):
        yield line

def filter_empty(lines):
    for line in lines:
        if line.strip():
            yield line.strip()

def upper_all(lines):
    for line in lines:
        yield line.upper()

data = "hello" + chr(10) + "world" + chr(10) + "" + chr(10) + "python"
pipeline = upper_all(filter_empty(read_lines(data)))
for item in pipeline:
    print(item)