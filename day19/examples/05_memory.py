# Memory comparison
import sys
big_list = [x**2 for x in range(100000)]
big_gen = (x**2 for x in range(100000))
print("List:", sys.getsizeof(big_list), "bytes")
print("Gen:", sys.getsizeof(big_gen), "bytes")