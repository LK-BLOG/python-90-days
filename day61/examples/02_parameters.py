# -*- coding: utf-8 -*-
import random
def simulate(text, temperature=0.7, n=50):
    words = ["Python","是","编程语言","简洁","优雅","强大","数据","科学"]
    result = []
    for _ in range(n):
        if temperature < 0.3: w = words[0]
        elif temperature < 0.8: w = random.choice(words[:4])
        else: w = random.choice(words)
        result.append(w)
    return "".join(result)
if __name__ == "__main__":
    for t in [0.1, 0.7, 1.5]:
        print(f"\nTemperature={t}: {simulate('Python', t)}")
