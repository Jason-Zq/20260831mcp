# 检索器（Retriever）是一种接口，能够根据非结构化查询返回文档。它的功能比向量存储更通用。检索器不需要具备存储文档的能力，只需能够返回文档即可。

# 检索器可以由向量存储构建，也可以由其他数据源构建，因此使用范围更广。

# 检索器接受字符串形式的查询作为输入，并返回一个由文档对象组成的列表作为输出。


# 5.1 VectorStore转Retriever
# 需要注意的是，所有VectorStore都可以转换为检索器。

# VectorStore提供as_retriever()方法将其转换为检索器，可以把调用VectorStore时的参数提前固化，简化后期的查询。

# 例如，每次我们都要传入k=3作为参数，我们就可以将其固化，转vectorstore为一个固定每次最多查3条数据的retriever：

# retriever = vectorstore.as_retriever(
#     search_type="similarity",  # 检索类型: similarity, mmr, similarity_score_threshold
#     search_kwargs={"k": 3}     # 返回top-3结果
# )

# 以后每次查询就可以直接使用retriever了

# 使用检索器检索
# retrieved_docs = retriever.invoke(query)

# print(f"查询: {query}\n")
# for i, doc in enumerate(retrieved_docs):
#     print(f"文档 {i+1}: {doc.page_content}")

# 当然，除了k以外，你也可以固化更多参数VectorStore支持的参数。但需要注意的是，Retirevers是不会返回得分的。



