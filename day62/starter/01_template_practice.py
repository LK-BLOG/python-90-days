# -*- coding: utf-8 -*-
import re
class PromptTemplate:
    def __init__(self, template_str):
        self.template_str = template_str
        self.variables = re.findall(r'\{(\w+)\}', template_str)
    def render(self, **kwargs):
        # TODO: 检查变量并替换
        pass
    def partial(self, **kwargs):
        # TODO: 部分填充，返回新模板
        pass

def build_translate_prompt(text, src, tgt):
    # TODO: 构建翻译prompt
    pass

def build_few_shot_prompt(examples, query):
    # TODO: 构建few-shot prompt
    pass

if __name__ == "__main__":
    t = PromptTemplate("你好 {name}，你是{role}")
    print(t.render(name="小明", role="学生"))
