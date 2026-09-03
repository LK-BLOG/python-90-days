# -*- coding: utf-8 -*-
def count_simple(text):
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return cn + (len(text)-cn)//4 + 1
def calc_cost(tok_in, tok_out, model="mini"):
    prices = {"gpt4o":(2.5,10.0),"mini":(0.15,0.60)}
    p = prices[model]
    return (tok_in*p[0]+tok_out*p[1])/1_000_000
if __name__ == "__main__":
    print(f"Token: {count_simple('Python是编程语言')}")
    print(f"Cost: ${calc_cost(1000,500):.6f}")
