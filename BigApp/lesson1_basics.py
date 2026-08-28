import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 请在此处填入你的真实 API Key (和 rag_demo 里的一样)
API_KEY = "sk-4e969c60e870461e8ae5b5aa14f53848"

print("=========================================")
print("🟢 第一关：用 LangChain 的方式连接大模型")
print("=========================================\n")

# ---------------------------------------------------------
# 1. 初始化模型 (相当于原生 SDK 里的 client = OpenAI(...))
# ---------------------------------------------------------
# 在 LangChain 里，聊天模型统一使用 Chat 类的包装器。
# 这里使用 ChatOpenAI 是因为 DeepSeek 的接口兼容 OpenAI 格式。
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

print("👉 测试 1: 最原始的提问方式")
# 注意：原生 SDK 叫 client.chat.completions.create(...)
# 而在 LangChain 里，万物皆可 .invoke() （调用/触发的意思）
response = llm.invoke("用一句简短的话形容学编程的心情。")

# 返回的不再是单纯的字符串，而是一个 AIMessage 对象，真实的文本在 .content 里
print(f"🤖 AI 回答: {response.content}\n")


# ---------------------------------------------------------
# 2. 提示词模板 (PromptTemplate)
# ---------------------------------------------------------
# 原生 Python 里你会用 f-string ( f"你好 {name}" )
# 但在复杂的 AI 应用里，提示词可能会长达几百行，用模板管理会更清晰。
print("👉 测试 2: 使用提示词模板插入变量")
prompt_template = PromptTemplate.from_template(
    "你是一个资深导游。请用非常浮夸的语气，用最多2句话向游客介绍【{city}】这个城市。"
)

# .format() 会自动把变量替换进去
formatted_prompt = prompt_template.format(city="重庆")
print(f"📝 组装好的提示词是: \n{formatted_prompt}\n")

# 发送给大模型
response2 = llm.invoke(formatted_prompt)
print(f"🤖 AI 回答: {response2.content}\n")

print("✅ 第一关执行完毕！去看看代码吧。")
