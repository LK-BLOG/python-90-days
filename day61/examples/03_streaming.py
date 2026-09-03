# -*- coding: utf-8 -*-
import time
def stream_text(text, delay=0.03):
    for c in text:
        yield c
        time.sleep(delay)
if __name__ == "__main__":
    for c in stream_text("Python是一门优雅的编程语言"):
        print(c, end="", flush=True)
    print()
