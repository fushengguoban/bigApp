import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

# ================= 1. 加载本地私有文档 =================
print("1. 正在读取本地机密文件...")
loader = TextLoader("company_secret.txt", encoding="utf-8")
docs = loader.load()

# ================= 2. 将长文档切片 (Chunking) =================
# 为什么要切片？因为整本书太长塞不进大模型，必须切成小块才能按需搜索
print("2. 正在将文档切成小碎块...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
splits = text_splitter.split_documents(docs)

# ================= 3. 向量化并存入 Chroma 数据库 =================
# 提示：首次运行会自动下载一个极小的开源嵌入模型(约80MB)，用于把汉字变成向量。
# 如果你运行报错提示缺少 sentence-transformers，请在终端执行: pip install sentence-transformers
print("3. 正在将文字转化为向量，存入本地 Chroma 数据库... (首次运行需等待几秒下载模型)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# ================= 4. 初始化大模型大脑 =================
print("4. 正在连接 DeepSeek 大脑...")
llm = ChatOpenAI(
    api_key="", # 填入你的真实 Key
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# ================= 5. 定义 RAG 核心提示词 (Prompt) =================
# 这就是 RAG 的精髓所在：把检索到的内容强行塞给 AI 的 Prompt 里
prompt = PromptTemplate.from_template("""
你是一个公司内部智能助手。请严格根据下面的【参考资料】来回答用户的问题。
如果你在资料里找不到答案，就回答“对不起，我不知道”，绝不能自己瞎编。

【参考资料】：
{context}

用户问题：{input}
""")

# ================= 6. 组装 LangChain 检索链 =================
# 这部分就是 LangChain 框架的威力，帮我们把检索和提问全部打包成了一条自动化的“链条”
print("5. 正在组装 LangChain 检索链...\n")
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)

# ================= 7. 开始提问测试！ =================
questions = [
    "研发部的 WiFi 密码是什么？",
    "服务器崩了找谁？他的微信号是多少？",
    "公司的董事长是谁？" # 这个问题文档里没有，测试它会不会瞎编
]

print("="*50)
for q in questions:
    print(f"👨‍💻 用户提问: {q}")
    # 这里会自动发生：去 Chroma 搜索相关片段 -> 替换到 Prompt 的 {context} 里 -> 发给大模型
    response = rag_chain.invoke({"input": q}) 
    print(f"🤖 助手回答: {response['answer']}\n")
    print("-" * 50)
