########################################PDF 阅读详解#############################
# 流程如下：
# PDF 文档 ──► pypdf 加载 ──► 分割(RecursiveCharacter) ──► 向量化入库(Chroma)
#                                                                  │
# 用户提问 ──────────────────────► 向量检索 (Retriever, k=3~5) ───┘
#                                        │
#                                        ▼
#                        防幻觉 Prompt + LLM ──► 生成回答 (Answer)
#
#
#
#
#
###############################################################################
import os
import time

from dotenv import load_dotenv
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

import more_learn_txt
from demo.lesson17_cost_effective_agent import search_web

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.3
)

CHROMA_PERSIST_DIR = "./chroma_board_api_db"  # 向量库本地保存路径
# 调优参数旋钮
CHUNK_SIZE = 400  # 每个片段字符数（调小可提升精确度，调大可增强上下文连贯性）
CHUNK_OVERLAP = 60  # 重叠长度（建议 15%~20%，避免语义从中间被切断）
RETRIEVER_K = 4  # 每次提问召回的文档片段数（k 值）
TEMPERATURE = 0.1  # 严禁大模型发散，越低事实一致性越好

# 2. 初始化 Embedding 模型（用作向量库存储）
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",  # 或者用 "BAAI/bge-small-zh-v1.5"
    encode_kwargs={"normalize_embeddings": True}
)

# DeepSeek 对话模型
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
    model="deepseek-chat",
    temperature=TEMPERATURE
)


# 构建本地向量库
def get_or_create_vector_db():
    # 如果本地已经有切好存好的向量库，直接加载，不重复消耗算力
    if os.path.exists(CHROMA_PERSIST_DIR) and len(os.listdir(CHROMA_PERSIST_DIR)) > 0:
        print(f"发现本地已存在向量库，正在直接加载: {CHROMA_PERSIST_DIR}...")
        return Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embedding_model
        )
    print(f"📄 正在使用 PyMuPDF 高速加载 PDF")
    start_time = time.time()
    loader = PyMuPDFLoader(f"F:\金通科技文档\sdkapi-v20201022-r20230522\主板API编程手册(20230522).pdf")
    pages = loader.load()
    total_pages = len(pages)
    print(f"✅ 加载成功！这本 PDF 一共有 {total_pages} 页。")
    print(f"✅ PDF 加载完成！共 {len(pages)} 页，耗时: {time.time() - start_time:.2f}s")

    # 针对中文与技术文档的分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " "]
    )
    split_docs = text_splitter.split_documents(pages)
    print(f"✂️ 文本分割完成！共切分为 {len(split_docs)} 个片段。")

    # 向向量库里面存储
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=CHROMA_PERSIST_DIR
    )
    print("向量库持久化构建完成")
    return vector_db


vector_db = get_or_create_vector_db()
retriever = vector_db.as_retriever({"k": RETRIEVER_K})

prompt_template = ChatPromptTemplate.from_template("""
你是一个严谨的嵌入式主板 API 技术支持工程师。请严格根据以下提供的参考文档内容回答用户问题。
回答规范：
1. 答案必须完全忠实于参考文档，严禁凭空捏造 API 函数名、参数或错误码；
2. 如果参考文档中未提及用户询问的功能，请明确回复：“手册中未找到相关 API 或说明”；
3. 回答应分点列出（如：功能描述、函数原型、主要参数、返回值等），条理清晰。
【参考文档片段】：
{context}
【技术咨询问题】：
{question}
""")
