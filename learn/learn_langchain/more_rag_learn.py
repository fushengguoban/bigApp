########################################RAG 深入学习#############################
# 1.RAG 简介：
# RAG 就是让大模型有东西可依靠   解决大模型原生痛点：知识滞后性，实时性差
# 适用场景：1.企业内部知识库问答，2.行业报告/政策分析 3.最新消息问答，4私有数据问答
# 不适用场景：1.创造性任务，2.逻辑推理任务，3。简单闲聊
#
# 标准场景： 文档加载-> 文本分割-> 向量存储->检索与生成
# RecursiveCharacterTextSplitter  作为默认分割器。 只能语意分割，
#
# 向量存储与嵌入 ，给文本做数字指纹
#
# 文本嵌入与向量存储完整流程
# 加载文档->分割文本->初始化嵌入模型->初始化向量数据库->将分割的文档嵌入并存储
#
#
#
#
#
#
###############################################################################
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

print("🤖 正在从本地硬盘加载离线重排模型，享受秒加载的快感...")

local_model_path = r"F:\AIDemo\models\bge-reranker-base"  # 👈 如果你的路径不一样，请修改这里！

model = HuggingFaceCrossEncoder(model_name=local_model_path)

# 向上跳3层：more_rag_learn.py -> learn_langchain -> learn -> BigApp
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# 推荐使用 Path 处理路径，避免跨系统兼容问题
text_path = BASE_DIR / "company_secret.txt"
loader = TextLoader(text_path, encoding="utf-8")

txt_docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,  # 重叠长度：建议为chunk_size的10%-20%，避免跨片段语义丢失
    length_function=len,
    separators=["\n\n", "\n", "。", "！", "？", "，", "；", "、"]  # 中文推荐分隔符优先级
)

# 3.执行分割
split_docs = text_splitter.split_documents(txt_docs)

print(f"原始文档数：{len(txt_docs)}")
print(f"分割后片段数：{len(split_docs)}")
print("\n前3个片段示例：")

for i, doc in enumerate(split_docs[:3]):
    print(f"\n片段{i + 1}（字符数：{len(doc.page_content)}）：")
    print(doc.page_content.strip())
    print(f"片段元数据：{doc.metadata}")  # 保留原始文档路径等元数据（检索时有用）

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", encode_kwargs={
    "normalize_embeddings": True
})

try:
    vector_db = FAISS.from_documents(
        documents=split_docs,
        embedding=embedding_model
    )
    # 持久化向量库到本地
    vector_db.save_local(
        folder_path="./faiss_db",
        index_name="local_cpu_faiss_index"
    )
    print("向量存储完成！向量数据已经保存到本地")
except Exception as e:
    raise RuntimeError(f"构建/保存向量库失败：{str(e)}")

query = "隋朝干了什么？"

try:
    retrieved_docs_with_scores = vector_db.similarity_search_with_score(query, k=3)
    print(f"\n与问题「{query}」最相关的3个文本片段：")

    for i, (doc, score) in enumerate(retrieved_docs_with_scores):
        print(f"\n片段{i + 1}：")
        print(f"内容：{doc.page_content}")
        print(f"相关性评分（越小越相似）：{round(score, 4)}")
        print(f"来源：{doc.metadata.get('source', '未知')}")
except Exception as e:
    raise RuntimeError(f"检索向量库失败：{str(e)}")
