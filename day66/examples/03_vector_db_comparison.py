# -*- coding: utf-8 -*-
DBS = {
    "ChromaDB": "本地, 小型, 原型开发",
    "FAISS": "本地, 大规模, 高性能",
    "Pinecone": "云, 大规模, 生产环境",
    "Weaviate": "云/本地, 多模态, GraphQL",
}
if __name__ == "__main__":
    for name, desc in DBS.items():
        print(f"{name}: {desc}")
