import os
import logging
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 开启日志，这样你能看到大模型是怎么“改写”你的问题的
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

print("======================================================")
print("🚀 启动究极 RAG 检索引擎：Multi-Query (扩写) + Reranker (重排)")
print("======================================================\n")

# 1. 准备大模型 (用于 Multi-Query 提问改写，这里沿用你 lesson9 的配置)
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf" 
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# 2. 准备刁钻的假数据
docs = [
    Document(page_content="公司考勤规章：如遇不可抗力导致的通勤受阻，需提交属地居委会的物理书面佐证。"),
    Document(page_content="设备维护指南：终端散热模块处于高负载警戒线时，应立即切断主电源以防主板熔毁。"),
    Document(page_content="餐厅就餐提示：食堂由于排气扇损坏，目前温度较高，大家就像在煎鸡蛋一样热，请谅解。"), # 干扰项！字面有煎鸡蛋和热
    Document(page_content="薪酬保密协议：禁止任何同级职员在非正式场合进行薪资结构的比对及探讨。")
]

print("📥 正在初始化底层向量库...")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

# 3. 构建“初筛”检索器 (捞取较多文档，比如前 3 个)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 4. 构建“第一层装甲”：Multi-Query 检索器 (让大模型扩写问题，增加召回率)
# 注意：我们把 base_retriever 包裹在了里面
mq_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)

# 5. 构建“第二层装甲”：Reranker 重排引擎 (精准度判卷，剔除干扰项)
print("🧠 正在加载 Reranker 判卷模型...")
rerank_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=rerank_model, top_n=1) # 最终只保留最准确的 1 篇

# 【核心缝合步骤】：把 mq_retriever (负责扩写和初捞) 包裹进重排引擎里！
super_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=mq_retriever
)

# 6. 开始测试！
user_question = "手机烫得能煎鸡蛋了咋办？"
print(f"\n🙋‍♂️ 用户提问: '{user_question}'")
print("\n⚙️ 检索引擎开始工作 (请观察上方绿色的日志，看它改写了什么问题)...\n")

# 调用究极检索器
final_docs = super_retriever.invoke(user_question)

print("\n🏆 经过 [大模型多路改写] + [向量库海选初捞] + [Reranker交叉精排] 后，最终胜出的文档是：")
for i, doc in enumerate(final_docs):
    print(f"   👑 第 {i+1} 名: {doc.page_content}")

print("\n🎉 恭喜！你已经掌握了目前业界最主流的高级 RAG 检索架构！")
