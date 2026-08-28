import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

print("=========================================")
print("⚖️ 启动精准度核武器：Reranker 重排引擎")
print("=========================================\n")

# 1. 准备极度容易混淆的假数据
docs = [
    Document(page_content="苹果公司的最新财报显示，iPhone销量超预期。"),  # 毫不相干，但字面有苹果
    Document(page_content="我在菜市场买了一斤红富士，非常甜。"),  # 字面有苹果，是水果
    Document(page_content="乔布斯是Apple这家伟大科技公司的创始人。")  # 正确答案，但连“苹果”两个字都没提！
]

print("📥 正在把数据存入底层向量库...")

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

user_question = "谁创立了那个卖iPhone的水果公司？"
print(f"\n🙋‍♂️ 用户提问: '{user_question}'\n")

# ---------------------------------------------------------
# 对比 1：基础向量检索 (初筛)
# ---------------------------------------------------------
print("❌ [初筛] 基础向量检索结果：")
# 取出全部 3 条结果，看看它们的原始排名
basic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
basic_docs = basic_retriever.invoke(user_question)

for i, doc in enumerate(basic_docs):
    print(f"   排名 {i + 1}: {doc.page_content}")

# ---------------------------------------------------------
# 对比 2：高级重排引擎 (Reranking)
# ---------------------------------------------------------
print("\n✅ [精排] 启动判卷模型进行交叉比对...")

rerank_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

compressor = CrossEncoderReranker(model=rerank_model, top_n=1)

advanced_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever = basic_retriever
)

# 再次发起查询
advanced_docs = advanced_retriever.invoke(user_question)
print("\n🎯 重排后，最终被选中的冠军文档是：")
for doc in advanced_docs:
    print(f"   👑: {doc.page_content}")
