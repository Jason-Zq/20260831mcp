# 3.1.4 基于Middleware实现查询优化
# 最后，我们来看看如何把查询优化组合到Agent中。
# 查询优化是对用户问题的重写，可以利用Middleware来实现

from typing import Any
from langchain.chat_models import init_chat_model
from langchain.agents import AgentState
from langchain_core.vectorstores import VectorStore
from langchain.messages import AIMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
import os
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.agents.middleware import AgentMiddleware, Runtime
from dotenv import load_dotenv
load_dotenv()


md_path = os.path.join(os.path.dirname(__file__), "中二知识笔记.md")

# 读取markdown数据
docs = ""
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    docs = "".join(line for line in lines)

# 切分依据，这里是按照三级标题
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
# 创建切分器
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

# 切分文档
chunks = markdown_splitter.split_text(docs)


idx = 1
# 定义方法，用来给文档内容拼上三级标题，让文档不丢失其所属章节，顺便加个id
def handle_doc_header(doc: Document):
    global idx
    m = doc.metadata
    doc.page_content = f"### {m['Header 3']}\n{doc.page_content}"
    doc.id = f"doc_{idx}"
    idx = idx + 1
    return doc
ds = [handle_doc_header(doc) for doc in chunks]

# 创建向量库和检索器
embeddings = DashScopeEmbeddings(
    model="qwen3.7-text-embedding", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
vectorstore = InMemoryVectorStore(embeddings)

# 添加文档
vectorstore.add_documents(ds)

print(f"知识库已就绪，{len(chunks)} 个文档")

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})



# 定义一个用于重写用户问题的模型，可以使用便宜的小模型
rewrite_llm = init_chat_model("deepseek-chat")


# 定义重写用户问题的Middleware
class QueryRewriteMiddleware(AgentMiddleware):
    """先改写查询再检索"""

    def __init__(self, vector_store: VectorStore, llm, top_k: int = 3):
        super().__init__()
        self.vector_store = vector_store
        self.llm = llm
        self.top_k = top_k

    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        messages = state.get("messages", [])
        if not messages:
            return None

        last_message = messages[-1]
        query = last_message.content if hasattr(last_message, 'content') else str(last_message)

        # Step 1: 重写查询

        ## 1.1.编写提示词
        rewrite_prompt = f"""
将以下问题改写为适合检索的关键词形式。提取核心概念，用空格分隔。只输出关键词不要解释。

问题: {query}
关键词:
"""
        ## 1.2.调用模型，重写用户问题
        rewritten = self.llm.invoke(rewrite_prompt).content.strip()
        print(f"[Rewrite] '{query[:40]}...' -> '{rewritten}'")
        print("=" * 60)

        # Step 2: 用改写后的查询检索
        ## 2.1.检索文档
        retrieved_docs = self.vector_store.similarity_search(query=rewritten, k=self.top_k)
        if not retrieved_docs:
            return None

        docs_content = "\n\n".join(
            f"[{d.metadata.get('source', '?')}] {d.page_content}" for d in retrieved_docs
        )

        print(f"检索到文档：{docs_content}")
        print("=" * 60)
        ## 2.2.拼接为新提示词并返回
        augmented = f"{query}\n\n请根据以下上下文回答：\n{docs_content}"

        return {
            "messages": [last_message.model_copy(update={"content": augmented})]
        }

rewrite_middleware = QueryRewriteMiddleware(vectorstore, rewrite_llm)


# 测试查询改写
rewrite_agent = create_agent(
    model="deepseek-chat",
    middleware=[rewrite_middleware],
    system_prompt="你是一个知识助手，请务必基于上下文回答用户问题，不要自己拓展。最后记得给出引用的原文内容。",
)

# 用口语化问题测试
response = rewrite_agent.invoke(
    {"messages": [{"role": "user", "content": "谁提出了教育要因材施教、启发诱导？其完整思想是什么？"}]},
)
print(f"回答: {response['messages'][-1].content}")