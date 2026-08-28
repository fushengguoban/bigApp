import os
import logging

from ddgs.api_server.api import search_text
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents import Document

logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

print("=========================================")
print("🔍 启动高级 RAG 检索引擎 (Multi-Query)")
print("=========================================\n")

# 1. 准备大模型
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf"
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# 2. 准备向量数据库和“刁钻”的假数据
print("📥 正在把极度官方、晦涩的文档存入向量库...")
docs = [
    Document(page_content="公司考勤规章：如遇不可抗力导致的通勤受阻，需提交属地居委会的物理书面佐证。"),
    Document(page_content="设备维护指南：终端散热模块处于高负载警戒线时，应立即切断主电源以防主板熔毁。"),
    Document(page_content="薪酬保密协议：禁止任何同级职员在非正式场合进行薪资结构的比对及探讨。")
]

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

user_question = "手机烫得能煎鸡蛋了咋办？"
print(f"\n🙋‍♂️ 用户提问: '{user_question}'\n")

print("❌ [基础 RAG] 正在仅凭字面意思进行盲搜...")
basic_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 1, "score_threshold": 0.3})
basic_docs = basic_retriever.invoke(user_question)

if basic_docs:
    print(f"   搜到的内容是: {basic_docs[0].page_content}")
else:
    print("   什么都没搜到。")

# ---------------------------------------------------------
# 对比 2：高级 RAG - Multi-Query (多查询智能扩展)
# ---------------------------------------------------------
print("\n✅ [高级 RAG] 启用 Multi-Query 智能扩展检索...")

# 这行代码是高级架构的灵魂！
# 我们把原本的初级检索器，交给了大模型 (llm) 去代理。
advanced_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_type="similarity_score_threshold",
                                       search_kwargs={"k": 1, "score_threshold": 0.3}   ),
    llm=llm
)
advanced_docs = advanced_retriever.invoke(user_question)

print("\n🎯 高级 RAG 最终成功捞取的文档集合：")

for i, doc in enumerate(advanced_docs):
    print(f"   第 {i + 1} 条: {doc.page_content}")

print("\n🎉 第九关代码执行完毕！看一眼日志，它是怎么拓展你的提问的？")
