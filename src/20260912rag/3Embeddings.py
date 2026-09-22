from langchain_ollama import OllamaEmbeddings
import numpy as np
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv() 

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# 创建Embedding模型
ollama_embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # 性价比高的模型
    dimensions=1024  # 可选：减少维度以节省存储
)

# # 向量化单条文本
# text = "我爱上班"
# vector = ollama_embeddings.embed_query(text)

# print(f"文本: {text}")
# print(f"向量维度: {len(vector)}")
# print(f"向量前5维: {vector[:5]}")

# # 批量向量化
# texts = ["我要躺平", "我爱工作", "拒绝加班"]
# vectors = ollama_embeddings.embed_documents(texts)
# print(f"\n批量向量化: {len(vectors)} 条, 维度: {len(vectors[0])}")


# # 比较向量相似度，值越大越相似
# for v in vectors:
#     similarity = cosine_similarity(vector, v)
#     print("Cosine Similarity:", similarity)





# # 使用阿里云百炼的Embedding服务
# from langchain_community.embeddings import DashScopeEmbeddings
# import os

# dashscope_embeddings = DashScopeEmbeddings(
#     model="qwen3.7-text-embedding",
#     dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
# )

# # 向量化单条文本
# text = "我爱上班"
# vector = dashscope_embeddings.embed_query(text)

# print(f"文本: {text}")
# print(f"向量维度: {len(vector)}")
# print(f"向量前5维: {vector[:5]}")

# # 批量向量化
# texts = ["我要躺平", "我爱工作", "拒绝加班"]
# vectors = dashscope_embeddings.embed_documents(texts)
# print(f"\n批量向量化: {len(vectors)} 条, 维度: {len(vectors[0])}")

# for v in vectors:
#     similarity = cosine_similarity(vector, v)
#     print("Cosine Similarity:", similarity)


