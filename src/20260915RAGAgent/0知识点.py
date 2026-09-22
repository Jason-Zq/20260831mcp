# 2.1 2-Step RAG
# 2-Step架构非常简单，就是严格遵循RAG流程：

# 把RAG的流程固化为两步：
# 1. Retrieve：检索知识库，返回知识片段
# 2. Generate：增强生成，基于知识片段增强Prompt和用户问题，调用模型生成答案

# 那么，问题来了：
# 我们如何在每次调用模型前增加知识检索的逻辑呢？

# 根据之前LangChain中所学的知识，要在调用模型之前做一件事情，有两种办法：
# - 利用@before_model这个Middleware装饰器，在每次调用模型前都执行知识检索，修改Prompt
# - 利用@dynamic_prompt这个Middleware装饰器，在每次调用前检索知识库，动态修改Prompt

# 这里我们以@dynamic_prompt为例：