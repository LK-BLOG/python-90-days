# -*- coding: utf-8 -*-
# 预测下面代码的输出，然后运行验证
x = 1
def foo():
    x = 2
    def bar():
        x = 3
        print("bar:", x)
    bar()
    print("foo:", x)
foo()
print("global:", x)
