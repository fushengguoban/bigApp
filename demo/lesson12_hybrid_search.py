import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

print("======================================================")
print("⚖️ 启动大厂级高性价比平替：混合检索 (BM25 + 向量)")
print("======================================================\n")

# 1. 准备极度容易混淆的假数据
docs = [
    Document(page_content="苹果公司的最新财报显示，iPhone销量超预期。"), 
    Document(page_content="我在菜市场买了一斤红富士，非常甜。"), 
    Document(page_content="乔布斯是这家伟大科技公司的创始人。") 
]

print("📥 [向量库] 正在进行语义特征提取并存入向量库...")
# --- 第一路召回：向量检索 (Dense Retrieval) ---
# 负责找“语义相近”的，能听懂言外之意
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


print("📥 [BM25库] 正在建立传统的全文索引库...")
# --- 第二路召回：全文检索 (Sparse Retrieval) ---
# 负责找“字眼精准匹配”的，绝不放过任何一个死角
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 2  # 同样每次捞出前 2 名


print("🔗 正在把向量检索和 BM25 组装成【混合检索器】...")
# --- 组合：混合检索器 (Ensemble) ---
# 将两路召回的结果混合，按权重打分去重
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]  # 权重各占一半，也可以调整成比如 0.3 和 0.7
)

# ---------------------------------------------------------
# 测试环节：我们来测一个刁钻的问题
# ---------------------------------------------------------
user_question = "这家伟大科技公司的财报和红富士苹果有关系吗？"
print(f"\n🙋‍♂️ 用户提问: '{user_question}'\n")

print("🔍 混合检索器开始工作...")
# 调用混合检索
final_docs = hybrid_retriever.invoke(user_question)

print("\n🎯 最终召回的文档集合 (结合了字面匹配和语义理解)：")
for i, doc in enumerate(final_docs):
    print(f"   第 {i + 1} 条: {doc.page_content}")

print("\n🎉 运行成功！你看，我们一行大模型代码都没写，0 Token 成本就实现了两路高精度召回！")
