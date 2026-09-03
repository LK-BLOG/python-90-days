# Challenge 3: 依赖倒置

## 目标
实现遵循DIP的数据处理管道。

## 要求
1. 定义DataSource和DataSink抽象
2. 实现CSV/Json数据源
3. 实现Database/File数据汇
4. 构造函数注入
5. 测试验证可替换

## 验收
- [ ] 自由组合Source和Sink
- [ ] 不需要修改管道代码
