# RAG分为两大阶段：
# - 离线阶段：负责构建知识库
#   1. 知识加载：读取各种来源的知识库数据，解析、清洗数据，形成文档（Documents）。
#   2. 知识切分：把清洗后的知识文档切分成一个个的知识片段（Chunks）
#   3. 向量化：利用向量模型将知识片段转为向量，使得语义相近的文本在该向量空间中彼此邻近
#   4. 存储向量：像处理好的向量及对应的知识片段存入向量数据库
# - 在线阶段：负责检索知识，生成回答
#   1. 问题向量化：利用向量模型（必须与离线阶段同一个模型）将用户问题转为向量
#   2. 知识召回：在向量数据库中检索与问题向量最相似的文档的TopN
#   3. 生成回答：把检索到的知识片段与用户提问组织为新提示词，发给大模型，生成回答


# LangChain的RAG组件
# LangChain为了简化RAG的开发，为我们提供了大量组件，满足RAG每一个流程的实现。

# 主要的组件包括：
# - 离线阶段
#   1. 知识加载：LangChain提供了Document Loader组件
#   2. 知识切分：LangChain提供了Text Splitter组件
#   3. 向量化：LangChain提供了Embeddings接口，兼容各类向量模型
#   4. 存储向量：LangChain提供了VectorStore接口，兼容各类向量数据库
# - 在线阶段：负责检索知识，生成回答
#   1. 问题向量化：同样基于Embeddings模型接口
#   2. 知识召回：LangChain提供了Retrievers组件，简化知识片段的检索操作
#   3. 生成回答：直接调用模型即可



# LangChain提供了丰富的文档加载器（Document Loaders），支持从各种来源加载文档，例如：
# - Webpages: 将网页内容加载为Document，例如WebBaseLoader
# - PDFs: 将PDF文件加载为Document，例如PyPDF
# - CommonFiles: 各种常见文件类型加载为Document，例如TextLoader、CSVLoader
# - Social platforms: 从社交媒体加载文档，例如Twitter、Reddit
# - Messaging services: 从消息平台加载文档，例如Telegram、WhatsApp、Discord
# - Productivity tools: 从常用的生产力工具中加载文档，例如Figma、Github、Slack
# 更多文档加载器参考LangChain官网：https://docs.langchain.com/oss/python/integrations/document_loaders#all-document-loaders

# 虽然加载器各不相同，但都实现了BaseLoader接口，因此都具有两个通用方法：
# - load() : 一次性加载所有文档
# - lazy_load() : 基于流式传输懒加载文档，适用于大数据集
# 所有加载器都将原始数据转换为统一的 Document 对象，包含：
# - page_content: 文档内容
# - metadata: 元数据（如来源、页码等）



