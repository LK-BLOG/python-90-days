# Challenge 1: 基础API调用

## 目标
用OpenAI SDK和httpx分别实现一次对话调用，处理错误，打印Token用量。

## 要求
1. 用 openai 库实现 AsyncOpenAI 调用
2. 用 httpx 手动构造请求实现相同功能
3. 处理API错误（401、429、500等）
4. 打印 token 用量

## 提示
- AsyncOpenAI 需要 wait
- httpx 的 client.post() 返回 Response 对象
- aise_for_status() 可以自动抛出HTTP错误

## 验收
- [ ] 两种方式都能成功调用
- [ ] 错误时有合理提示
- [ ] Token用量被打印
