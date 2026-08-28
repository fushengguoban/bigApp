import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 你的 API Key
API_KEY = "sk-4e969c60e870461e8ae5b5aa14f53848"

print("=========================================")
print("🟣 第五关：开卷考试进阶 (RAG 拆解)")
print("=========================================\n")

# 在最开始你遇到的那个 rag_demo.py 里，
# 你用到了 create_retrieval_chain 和 create_stuff_documents_chain。
# 这些“黑盒”函数把你搞晕了。
# 今天，我们将用你在第二关学到的 LCEL (| 符号)，纯手工打造一条 RAG 流水线！
# 这样你就彻底懂得底层是怎么运作的了。

# 1. 准备资料库 (老规矩，读取你的 company_secret.txt)
print("1. 正在准备本地数据库...")
loader = TextLoader("company_secret.txt", encoding="utf-8")
splits = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20).split_documents(loader.load())
# 注意：如果你之前跑过 rag_demo.py，这里的模型你应该已经下载过了，会很快。
vectorstore = Chroma.from_documents(documents=splits, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

# 【非常重要】：将数据库变成一个“检索器 (retriever)”。
# 检索器的功能极其纯粹：你给它丢进去一段字符串，它就吐给你一堆最相关的文档碎片。
retriever = vectorstore.as_retriever()


# 2. 准备大脑和试卷 (模型与 Prompt)
llm = ChatOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1", model="deepseek-chat")

# 注意：试卷（Prompt）上我们留了两个空格
# {context} 用来填我们查到的复习资料
# {question} 用来填用户实际提出的问题
prompt = PromptTemplate.from_template("""
你是一个内部助手。请严格根据下面的【参考资料】回答问题。如果你在资料里找不到答案，就回答不知道，绝不能自己瞎编。

【参考资料】：
{context}

问题：{question}
""")


# 3. 终极魔法：用 LCEL (|) 拼装 RAG 流水线！
# 官网文档里的 RAG 最终都会长下面这个样子：

def format_docs(docs):
    # 这个小函数的作用只是把检索器吐出来的一堆碎片，用回车拼成一段完整的长字符串
    return "\n\n".join(doc.page_content for doc in docs)

print("2. 正在用 LCEL 拼装手工 RAG 流水线...")

# 请仔细看这条最经典的 LangChain 表达式：
rag_chain = (
    # 第一步：准备变量。
    # RunnablePassthrough() 的意思是“原封不动”。
    # 当用户提问时，问题会分成两路：
    # 一路原封不动传给 "question"。
    # 另一路传给 retriever 去搜索，搜到的结果经过 format_docs 处理后，传给 "context"。
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    
    # 第二步：把填好资料的试卷发给模型
    | prompt
    | llm
    
    # 第三步：剥离干净的文本输出
    | StrOutputParser()
)


# ----------------- 开始测试 -----------------
print("\n🧑 我: 咱们明年有什么新项目吗？")

# 你看，我们这次只需要传一句话进去。
# 流水线会自动把这句话拆分成搜索条件和 Prompt 问题！
response = rag_chain.invoke("咱们明年有什么新项目吗？")

print(f"🤖 AI: {response}\n")

print("✅ 第五关全部通关！你已经毕业了！")
