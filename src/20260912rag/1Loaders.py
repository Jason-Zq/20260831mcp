# 1.1 TextLoader
# TextLoader是社区提供的加载器，作用是加载普通的txt文件，这也是最常见的一种文本文件类型，格式简单，没什么好说的，直接看代码。

# from langchain_community.document_loaders import TextLoader
# import os

# txt_path = os.path.join(os.path.dirname(__file__), "sample.txt")

# # 创建示例文本文件
# with open(txt_path, "w", encoding="utf-8") as f:
#     f.write("LangChain是用于构建LLM应用的框架。\n")
#     f.write("LangGraph是LangChain的图结构编排库。\n")
#     f.write("LangSmith是调试监控平台。\n")

# # 加载文本文件
# loader = TextLoader(txt_path, encoding="utf-8")
# docs = loader.load()

# print(f"加载了 {len(docs)} 个文档")
# print(f"内容: {docs[0].page_content}")
# print(f"元数据: {docs[0].metadata}")


# 1.2 WebBaseLoader
# WebBaseLoader同样是社区提供的加载器，只要给一个url地址，它就能自动读取网页内容，去掉无用的Html、CSS、JS元素，只保留普通文本数据。

# from langchain_community.document_loaders import WebBaseLoader

# # 加载网页内容
# loader = WebBaseLoader(
#     web_paths=["https://docs.langchain.com/oss/python/langchain/rag"],
# )
# docs = loader.load()

# print(f"加载了 {len(docs)} 个文档")
# print(f"来源: {docs[0].metadata.get('source', 'unknown')}")
# print(f"内容长度: {len(docs[0].page_content)} 字符")
# print(f"内容预览: {docs[0].page_content[:200]}...")


# 1.3 CSVLoader
# CSVLoader也是社区提供的加载器，它可以加载csv格式的文件, 类似Excel (xlsx) 

# from langchain_community.document_loaders.csv_loader import CSVLoader
# import csv
# import os

# csv_path = os.path.join(os.path.dirname(__file__), "sample.csv")

# with open(csv_path, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["name", "description", "category"])
#     writer.writerow(["LangChain", "LLM应用开发框架", "AI框架"])
#     writer.writerow(["LangGraph", "图结构编排库", "AI框架"])
#     writer.writerow(["LangSmith", "调试监控平台", "AI工具"])

# # 加载CSV文件
# loader = CSVLoader(
#     file_path=csv_path,
#     source_column="name",  # 用name列作为source
#     encoding="utf-8"
# )
# docs = loader.load()

# print(f"加载了 {len(docs)} 行数据")
# for doc in docs:
#     print(f"  [{doc.metadata.get('source', '?')}] {doc.page_content[:100]}")



# 1.4 PyPDFLoader
# PyPDFLoader顾名思义，是加载PDF文件的加载器，依赖于pypdf，所以需要先安装：
# uv add pypdf
# PyPDFLoader支持两种模式：
# - single：整个文档作为一个Document，但是可以自定义文档页与页之间的分隔符
# - page：每页作为一个Document

# from langchain_community.document_loaders import PyPDFLoader
# import os

# pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")

# # 加载PDF文件（整个文档作为一个Document）
# loader = PyPDFLoader(
#     pdf_path,
#     mode="single", # single \ page
#     pages_delimiter="\n-------THIS IS A CUSTOM END OF PAGE-------\n" # 自定义页分隔符，可选
# )
# docs = loader.load()

# print(f"加载了 {len(docs)} 页")
# print("-"*50)
# print(f"第1页内容: {docs[0].page_content[:15800]}...")
# print("-"*50)
# print(f"元数据: {docs[0].metadata}")  # 包含 source, page 等信息


# 1.5 复杂文本加载工具
# 某些行业的PDF文件结构非常复杂，可能包含：左右分栏、复杂表格、图文混排、图片扫描件等情况。
# 针对这样的PDF文件就需要用到诸如：文档结构识别模型、多模态模型、表格处理、OCR等专用工具，非常复杂。
# 好在市面上已经有很多专业的工具，帮我们实现了这些功能。

# 1.5.3 使用MinerU
# MinerU的API是基于Http协议，理论上我们可以直接基于Http请求调用。
# - SDK : 原生SDK，兼容性最好，可以自由的处理MinerU解析好的markdown、images、json
# - LangChain : 完美适配LangChain，但解析PDF时只能得到markdown，其它内容无法获取
# - Flash模式：


# from mineru.client import MinerU
# import os
# from dotenv import load_dotenv

# load_dotenv()

# Flash 模式，无需Token
# 创建客户端
# client = MinerU()

# pdf_path = os.path.join(os.path.dirname(__file__), "sample11111.pdf")

# # 解析文件
# result = client.flash_extract(pdf_path)

# md_path = os.path.join(os.path.dirname(__file__), "r2.md")
# # 输出到本地
# result.save_markdown(md_path)


# Precision模式，需要Token ，可以到官网申请 https://mineru.net
# 创建客户端
# client = MinerU(os.getenv("MINERU_TOKEN"))
# # 解析文件，支持各种自定义参数，例如：language、ocr、

# pdf_path = os.path.join(os.path.dirname(__file__), "sample2.pdf")

# # result = client.extract("https://cdn-mineru.openxlab.org.cn/demo/example.pdf")
# result = client.extract(pdf_path)
# # 输出到本地
# md_path = os.path.join(os.path.dirname(__file__), "r5.md")
# result.save_markdown(md_path, True)





# 1.5.3.2 基于LangChain
# 基于SDK方式虽然可以读取到图片，但输出格式只是普通文本。如果你的项目是基于LangChain，后续就需要我们自己把markdown封装为LangChain的Document.

# 所以，如果你的PDF不包含图片，或者图片中不包含重要信息，完全可以直接使用MinerU官方提供的LangChain版本SDK，解析完成后直接得到LangChain的Document对象。
# uv add langchain-mineru

# from langchain_mineru import MinerULoader
# import os
# from dotenv import load_dotenv

# load_dotenv()

# pdf_path = os.path.join(os.path.dirname(__file__), "sample11111.pdf")

# # 初始化客户端
# loader = MinerULoader(
#     source=pdf_path,
#     mode="flash" # 可选: flash 、 precision
# )
# # 解析文档，返回值直接是LangChain的 Document集合
# docs = loader.load()

# print(docs[0].metadata) # 元数据
# # print(docs[0].page_content) # 文档内容

# # 写到本地看看
# md_path = os.path.join(os.path.dirname(__file__), "r6.md")

# with open(md_path, "w", encoding="utf-8") as f:
#     f.write(docs[0].page_content)


# 1.5.3.3 OCR功能
# 对于扫描件类型的PDF，MinerU处理起来也毫不费力，只需要把OCR参数改为True即可：

from langchain_mineru import MinerULoader
import os
from dotenv import load_dotenv

load_dotenv()

pdf_path = os.path.join(os.path.dirname(__file__), "sample3.pdf")

# 初始化客户端
loader = MinerULoader(
    source=pdf_path,
    mode="precision",
    ocr=True  # 开启OCR功能
)
# 解析文档，返回值直接是LangChain的 Document集合
docs = loader.load()

print(docs[0].metadata) # 元数据
print(docs[0].page_content) # 文档内容

# 写到本地看看
md_path = os.path.join(os.path.dirname(__file__), "r7.md")

with open(md_path, "w", encoding="utf-8") as f:
    f.write(docs[0].page_content)