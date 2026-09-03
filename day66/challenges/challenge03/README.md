# 挑战三：FAISS索引构建

## 难度
★★★☆☆

## 项目名
FaissBuilder - FAISS索引构建与搜索

## 目标
使用FAISS库构建不同类型的向量索引，比较其性能和搜索质量。

## 背景
FAISS是Facebook开源的高效向量检索库，支持多种索引类型。本挑战让你掌握索引构建和优化。

## 功能要求
1. **索引构建**：支持Flat、IVF、HNSW三种索引类型
2. **向量添加**：批量添加向量到索引
3. **相似度搜索**：执行K近邻搜索
4. **性能比较**：测试不同索引的构建时间和搜索速度

## 输入
- 向量数据集：1000个8维向量
- 查询向量：8维numpy数组
- 索引类型参数

## 输出
- 搜索结果：最近邻向量的ID和距离
- 性能报告：构建时间和搜索时间

## 限制条件
- 使用FAISS库（可选，如无则模拟）
- 向量维度固定为8维
- 支持批量搜索

## 示例
`python
builder = FaissBuilder(dim=8)
index = builder.build_index(vectors, index_type="flat")
results = builder.search(query_vec, k=3)
print(f"搜索耗时: {builder.get_search_time():.4f}s")
`

## 验收标准
- [ ] 支持多种索引类型构建
- [ ] 向量添加功能正常
- [ ] K近邻搜索返回正确结果
- [ ] 性能测量功能正常
- [ ] 代码有中文注释

## 可选扩展
- 实现索引持久化
- 添加索引参数调优
- 支持增量索引更新
