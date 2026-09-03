# -*- coding: utf-8 -*-
def build_messages(system_prompt, user_message):
    # TODO: 返回消息列表 [{"role":"system","content":...}, {"role":"user","content":...}]
    pass

def calc_cost(input_tokens, output_tokens, in_price=0.15, out_price=0.60):
    # TODO: 计算费用 ($/1M tokens)
    pass

if __name__ == "__main__":
    print(build_messages("sys","usr"))
    print(f"${calc_cost(1000,500):.6f}")
