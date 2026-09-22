from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

import os
from dotenv import load_dotenv
load_dotenv()


# ===============一、构建知识库阶段====================
# =============1.加载文档===============

report_path = os.path.join(os.path.dirname(__file__), "荒坂集团2077年度财报.pdf")

loader = PyPDFLoader(
    report_path,
    mode="single", # single \ page
)
docs = loader.load()
print(f"文档数量:{len(docs)}")

# =============2.切分文档===============
# 创建递归切分器
splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=150)
# 切分文档
chunks = splitter.split_documents(docs)
print(f"分块数量：{len(chunks)}")

# =============3.向量化===============
# 向量模型，这里用阿里云的向量模型
embeddings = DashScopeEmbeddings(
    model="qwen3.7-text-embedding",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 创建向量库，需要指定向量模型，存储文档时会自动调用向量模型完成向量化
vectorstore = InMemoryVectorStore(embedding=embeddings)
# 添加文档
vectorstore.add_documents(chunks)


# ==============二、在线问答阶段================
llm = init_chat_model("deepseek-chat")

def try_rag(query: str):
    # 1.检索文档（VectorStore会自动把问题向量化，召回相关知识片段）
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    # 2.拼接上下文提示词
    content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = f"""你基于我提供的报告回答用户问题，报告中没提及的就说不知道，不要自己编造答案.
    report: ```{content}```
    query: {query}"""
    # 3.调用模型，生成答案
    response = llm.invoke(prompt)
    return response.content


print(try_rag("荒坂集团2077年度的市盈率和市净率是多少？"))