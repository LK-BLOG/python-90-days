# Generator expression
squares = (x**2 for x in range(10))
print(sum(squares))  # 285

# vs list comprehension (uses more memory)
squares_list = [x**2 for x in range(10)]
print(sum(squares_list))