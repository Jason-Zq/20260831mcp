
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
import os
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