from langchain_text_splitters import CharacterTextSplitter
import os


md_path = os.path.join(os.path.dirname(__file__), "r1.md")

content = ""
with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

# 准备一段较长的文本
long_text = content

# # 创建字符切分器
# text_splitter = CharacterTextSplitter(
#     separator="\n",    # 以换行符作为分隔
#     chunk_size=1000,     # 每块最大1000字符
#     chunk_overlap=200,   # 块之间重叠200字符
# )


# # 切分文本
# chunks = text_splitter.split_text(long_text)

# print(f"原始文本长度: {len(long_text)} 字符")
# print(f"切分为 {len(chunks)} 个块:\n")
# for i, chunk in enumerate(chunks):
#     print(f"--- Chunk {i+1} ({len(chunk)}字符) ---")
#     print(chunk)
#     print()


# 2.1.2 CharacterTextSplitter - 按Token切分
# 使用OpenAI开源的tiktoken计算token数量，按token数量切分，更精确地控制发送给LLM的token数。


# from langchain_text_splitters import CharacterTextSplitter

# 使用from_tiktoken_encoder，LangChain自带，无需额外安装tiktoken
# token_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#     encoding_name="cl100k_base",    # token分词器编码名
#     chunk_size=1000,                # 每块最多1000 token
#     chunk_overlap=200,              # 块之间重叠200字符
# )

# chunks = token_splitter.split_text(long_text)

# print(f"原始文本长度: {len(long_text)} 字符")
# print(f"切分为 {len(chunks)} 个块:\n")
# for i, chunk in enumerate(chunks):
#     print(f"--- Chunk {i+1} ({len(chunk)}字符) ---")
#     print(chunk)
#     print()


# 2.2 递归字符切分（推荐）
# LangChain中提供了一个RecursiveCharacterTextSplitter类，实现了递归字符切分。
# 这是LangChain推荐的通用文本切分器，在不超过目标块大小的前提下，尽可能保持段落和句子的完整性。

# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # 创建递归切分器
# recursive_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=2000,
#     chunk_overlap=200,
#     separators=["\n\n", "\n", "。"]  # 优先级从高到低
# )

# # 切分文档
# chunks = recursive_splitter.split_documents([Document(page_content=long_text)])

# print(f"切分为 {len(chunks)} 个块:\n")
# for i, split in enumerate(chunks):
#     print(f"--- Chunk {i+1} ({len(split.page_content)}字符) ---")
#     print(split.page_content)
#     print()


# 2.3 结构感知切分
# 利用文档元数据识别文档本身的逻辑区块进行切分。

# 例如：markdown中的多级标题、JSON结构中的字段、Html中的标签等等。

# LangChain都提供了对应不同文档类型的结构感知切分器，例如：
# - MarkdownHeaderTextSplitter
# - RecursiveJsonSplitter
# - HTMLHeaderTextSplitter
# - RecursiveCharacterTextSplitter.from_language()
# - ...
# 此处，我们以markdown为例来演示。

# from langchain_text_splitters import MarkdownHeaderTextSplitter

# # markdown数据
# markdown_document = "# 1.Foo\n\n    ## 1.1.Bar\n\nHi this is Jim\n\nHi this is Joe\n\n ### 1.1.1.Boo \n\n Hi this is Lance \n\n ## 1.2.Baz\n\n Hi this is Molly"

# # 切分依据，这里是按照三级标题
# headers_to_split_on = [
#     ("#", "Header 1"),
#     ("##", "Header 2"),
#     ("###", "Header 3"),
# ]

# # 创建切分器
# markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

# # 切分文档
# chunks = markdown_splitter.split_text(markdown_document)

# for doc in chunks:
#     print(doc.model_dump_json(indent=2))



# 2.4 总结
# 没有绝对正确的文档切分方式，一定要根据具体文档来具体判断。

# 如果你采用了MinerU这样的文本加载器，由于其输出的格式通常是Markdown，有严谨的文档结构，那我的建议切分方式是：
# - 优先采用Markdown的文档结构切分，不仅语义完整度高，而且还能记住自己所处的章节
# - 当基于文档结构切分的块太大时，可以对超过目标size的块采用递归字符切分，但要保留header到每一个分块