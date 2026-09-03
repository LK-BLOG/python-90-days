# Day 74: 智能文档助手 - 第一部分

## 架构
文档输入 -> 解析 -> 分块 -> 嵌入 -> 向量存储 + 元数据索引

## 文档解析
PDF: pdfplumber | DOCX: python-docx | HTML: BeautifulSoup

## 分块策略
段落感知 + 固定大小重叠, 保留上下文连贯性

## 索引构建
批量嵌入 -> ChromaDB -> 元数据过滤
