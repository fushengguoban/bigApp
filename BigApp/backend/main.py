import os
from fastapi import FastAPI, HTTPException
from langchain_classic.chains.hyde.prompts import web_search
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

import sqlite3

print("⚙️ [System] 正在初始化向量知识库...")
# 确保能够找到相对于 backend 目录上一级的 company_secret.txt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_path = os.path.join(BASE_DIR, "company_secret.txt")

try:
    loader = TextLoader(secret_path, encoding="utf-8")
    splits = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20).split_documents(loader.load())
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    retriever = vectorstore.as_retriever()
    print("✅ [System] 知识库初始化成功！")
except Exception as e:
    print(f"❌ [System] 知识库初始化失败，请确保 {secret_path} 存在。错误: {e}")
    retriever = None

# --- 大模型与 Agent 工具设置 ---
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf"
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)


@tool
def search_company_secrets(query: str) -> str:
    """当用户问到有关公司的内部规定、密码、新项目、人员等私有资料时，调用此工具进行搜索。"""
    if not retriever:
        return "本地知识库未初始化。"

    docs = retriever.invoke(query)
    # 将找到的资料合并成字符串返回给大模型
    return "\n\n".join(doc.page_content for doc in docs)


wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
web_search = DuckDuckGoSearchRun(api_wrapper=wrapper)
# 装配 Agent
tools = [search_company_secrets, web_search]
system_prompt = ("1.你是一个强大的AI助理。"
                 "2.如果遇到不知道的公司内部问题，必须使用 search_company_secrets 工具去查找。回答要友好且专业。"
                 "3.遇到外部世界问题（特别是查天气、查新闻等要求），绝对不准说你查不到,必须立刻使用 duckduckgo_search 工具去搜索")
# agent_executor = create_react_agent(llm, tools, prompt=system_prompt)
conn = sqlite3.connect("chat_histoty.db", check_same_thread=False)
memory_saver = SqliteSaver(conn)
memory_saver.setup()
agent_executor = create_react_agent(llm, tools, prompt=system_prompt, checkpointer=memory_saver)

# --- FastAPI 路由设置 ---
app = FastAPI(title="AI Search Assistant API")


# 定义前端传过来的数据格式
class ChatRequest(BaseModel):
    message: str
    session_id: str


# 定义返回给前端的数据格式
class ChatResponse(BaseModel):
    reply: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print(f"\n📩 [收到前端请求]: {request.message}")
    try:
        config = {"configurable": {"thread_id": request.session_id}}
        # 调用 LangGraph Agent 处理前端发来的消息
        response = agent_executor.invoke({"messages": [("user", request.message)]},
                                         config=config)

        # 提取最后一条回复作为答案
        final_answer = response["messages"][-1].content
        print(f"🤖 [返回前端答案]: {final_answer}")

        return ChatResponse(reply=final_answer)
    except Exception as e:
        print(f"❌ [处理报错]: {e}")
        raise HTTPException(status_code=500, detail=str(e))
