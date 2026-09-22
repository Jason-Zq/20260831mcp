
# LangChain提供了统一的VectorStore接口，使你可以用统一的方式调用任意向量库：
# - add_documents: 添加文档到向量库（不用自己做文本向量化，只要提供好向量模型即可）
# - delete: 根据id删除某个文档
# - similarity_search: 基于相似度检索与用户问题有关的文档

# 接下来，我们以Chroma为例讲解VectorStore的用法。


from langchain_chroma import Chroma
import os
from langchain_ollama import ollama_embeddings  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

db_path = os.path.join(os.path.dirname(__file__), "chroma_langchain_db")

# 创建向量库
vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=ollama_embeddings,
    persist_directory=db_path,
)


md_path = os.path.join(os.path.dirname(__file__), "r5.md")

# 准备文档，我们用之前读取的Markdown文档来测试
with open(md_path, encoding="utf-8") as f:
    markdown_text = "\n".join(line for line in f.readlines())


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "。"]  # 优先级从高到低
)

# 用递归切分器切分文档
chunks = recursive_splitter.split_documents(
    [Document(page_content=markdown_text, metadata={"filename": "r5.md"})]
)

print(f"  len: {chunks.__len__()}")

# 给文档生成id
ids=[]
for i,c in enumerate(chunks):
    c.id = f"doc_{i+1}"
    print(f"  id: {c.id}")
    c.metadata['id'] = c.id
    ids.append(c.id)
# 删除旧文档
vectorstore.delete(ids)
# 添加新文档
vectorstore.add_documents(chunks)



# 4.3 检索文档
# VectorStore提供了多个检索文档的方法，例如：
# - search: 通用搜索方法，支持最多样化的参数
# - similarity_search: 基于相似度的搜索
# - similarity_search_with_relevance_scores: 基于相似度搜索，并且会返回相似度得分


# # 用户问题
# query = "1.1的内容是什么？"
# # 相似度检索
# results = vectorstore.search(
#     query=query,
#     search_type="similarity",
#     k = 5,
# )

# print(f"查询: {query}\n")
# for i, doc in enumerate(results):
#     print(f"结果 {i+1}: {doc.page_content}")
#     print(f"  元数据: {doc.metadata}")



# 4.3.2 基于metadata过滤
# 我们还可以在检索时基于文档的metadata做过滤：

# 用户问题
# query = "1.2的内容是什么？"
# # 相似度检索
# results = vectorstore.search(
#     query=query,
#     search_type="similarity",
#     k = 5,
#     filter={"id": "doc_1"}
# )

# print(f"查询: {query}\n")
# for i, doc in enumerate(results):
#     print(f"结果 {i+1}: {doc.page_content}")
#     print(f"  元数据: {doc.metadata}")


# 4.3.3 带相似度得分的检索
# 如果调用VectorStore的similarity_search_with_score方法，还可以在检索时返回相似度打分：
# 用户问题
query = "住址是那里？"
# 相似度检索
results = vectorstore.similarity_search_with_relevance_scores(
    query=query,
    # search_type="similarity_score_threshold", 不需要search_type了
    score_threshold=0, # 只把相似度分数 ≥0.42 的检索结果留下来，低于 0.42 的直接丢掉，哪怕写了 k=5**
    k = 5
)

print(f"查询: {query}\n")
for doc, score in results:
    print(f"======文档: {doc.id}，得分：{score}=======")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")







# 获取底层chromadb原生collection对象
# coll = vectorstore._collection
# print("总记录数：", coll.count())

# 获取全部记录，不加载向量（推荐，省内存）
# all = coll.get(
#     limit=None,
#     offset=0,
#     include=["documents", "metadatas"] # 不要加embeddings，很大
# )

# res = coll.peek(100)  # 获取前100条记录，包含向量

# ids=[]
# # res里面有 ids、documents、metadatas，可选embeddings
# for idx, doc in enumerate(res["documents"]):
#     print(f"\n---id:{res['ids'][idx]}---")
#     ids.append(res['ids'][idx])

    # print("文本chunk：", doc)
    # print("元数据metadata：", res["metadatas"][idx])

# vectorstore.delete(ids)
