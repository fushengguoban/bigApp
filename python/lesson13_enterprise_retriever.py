import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

print("===================================================================")
print("🚀 启动终极版大厂检索引擎：混合检索(0 Token) + 本地模型精排")
print("===================================================================\n")

docs = [
    Document(page_content="苹果公司的最新财报显示，iPhone销量超预期。"), 
    Document(page_content="我在菜市场买了一斤红富士，非常甜。"), 
    Document(page_content="乔布斯是这家伟大科技公司的创始人。") 
]

print("📥 [1/3] 正在加载本地 Embedding 模型并构建两路初筛库...")
# 注意：你的 Embedding 其实也可以下载到本地然后换成本地路径！
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 
)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 3

hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)

print("🧠 [2/3] 正在加载【本地】Reranker 判卷模型...")
# 👈 这里换成了你的本地路径！极其优雅且适合国内开发环境
local_model_path = r"F:\AIDemo\models\bge-reranker-base"  
rerank_model = HuggingFaceCrossEncoder(model_name=local_model_path)
compressor = CrossEncoderReranker(model=rerank_model, top_n=1) 

print("🔗 [3/3] 正在缝合所有组件...")
# 究极组合：(BM25 + 向量) 混合初筛 -> 本地 Reranker 精排
ultimate_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=hybrid_retriever
)

user_question = "这家伟大科技公司的财报和红富士苹果有关系吗？"
print(f"\n🙋‍♂️ 用户提问: '{user_question}'\n")

print("🔍 终极检索引擎开始工作...")
final_docs = ultimate_retriever.invoke(user_question)

print("\n🎯 最终胜出的金牌文档是：")
for i, doc in enumerate(final_docs):
    print(f"   👑: {doc.page_content}")

print("\n🎉 完美！大厂最标准的检索流水线已经全部跑通！")
