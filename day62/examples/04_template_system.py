# -*- coding: utf-8 -*-
import re
class PromptTemplate:
    def __init__(self, template_str, variables=None):
        self.template_str = template_str
        self.variables = variables or re.findall(r'\{(\w+)\}', template_str)
    def render(self, **kwargs):
        missing = set(self.variables) - set(kwargs.keys())
        if missing: raise ValueError(f'缺少变量: {missing}')
        return self.template_str.format(**kwargs)
    def partial(self, **kwargs):
        new = self.template_str
        for k, v in kwargs.items():
            new = new.replace('{' + k + '}', v)
        remaining = re.findall(r'\{(\w+)\}', new)
        return PromptTemplate(new, remaining)

CLASSIFY = PromptTemplate("分类 {text} 为 {categories}")
TRANSLATE = PromptTemplate("将 {text} 从 {src} 翻译为 {tgt}")

if __name__ == "__main__":
    print(CLASSIFY.render(text="你好", categories="正面/负面"))
    t = TRANSLATE.partial(src="中文", tgt="英文")
    print(t.render(text="你好世界"))
