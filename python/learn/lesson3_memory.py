import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 你的 API Key
API_KEY = "sk-4e969c60e870461e8ae5b5aa14f53848"

print("=========================================")
print("🟠 第三关：过目不忘 (Memory)")
print("=========================================\n")

llm = ChatOpenAI(
    api_key=API_KEY, 
    base_url="https://api.deepseek.com/v1", 
    model="deepseek-chat"
)

# 1. 创建带有【聊天记录预留位置】的模板
# 在你的 web_chat.py 中，你是手动 list.append() 把聊天记录加进去的。
# 在 LangChain 里，我们用 MessagesPlaceholder 给历史记录留个“占位符”。
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个记性很好的朋友。"),
    MessagesPlaceholder(variable_name="history"), # <--- 流水线会自动把聊天记录塞到这里
    ("human", "{question}"),
])

# 2. 组装基础流水线 (此时它还没有记忆)
chain = prompt | llm | StrOutputParser()

# 3. 准备一个存储历史记录的“小本本” 
# 这是一个普通的字典，用来模拟数据库。实际开发中可以换成 Redis 记录或数据库记录。
store = {}

# 这个函数的作用是：当有人提问时，根据他的 session_id 去字典里找他之前的聊天记录
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 4. 把基础流水线包装成“带记忆的超级流水线”
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# ----------------- 开始测试 -----------------

print("🧑 我: 我叫林克，我喜欢塞尔达。")
# 注意这里的 config 参数，我们传了一个 session_id="user_123"
# 这样哪怕同时有 100 个人在跟你聊天，AI 也绝不会串台！
response1 = with_message_history.invoke(
    {"question": "我叫林克，我喜欢塞尔达。"},
    config={"configurable": {"session_id": "user_123"}} 
)
print(f"🤖 AI: {response1}\n")

# 第二次提问，看看它到底有没有记住！
print("🧑 我: 我叫什么名字？我喜欢什么？")
response2 = with_message_history.invoke(
    {"question": "我叫什么名字？我喜欢什么？"},
    config={"configurable": {"session_id": "user_123"}}
)
print(f"🤖 AI: {response2}\n")

print("✅ 第三关执行完毕！")
