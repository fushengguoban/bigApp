import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 你已经填好 Key 了，我直接拿过来了
API_KEY = "sk-4e969c60e870461e8ae5b5aa14f53848"

print("=========================================")
print("🟡 第二关：规矩与锁链 (Output Parsers & LCEL 初体验)")
print("=========================================\n")

llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

prompt = PromptTemplate.from_template("请用一句话夸奖一下【{language}】这门编程语言。")

print("👉 1. 回顾上一关的原始写法 (没有 LCEL)")
# 在上一关，我们要得到一段干净的文字，需要两步：
# 1) 手动 format 组装字符串
formatted_text = prompt.format(language="Python")
# 2) 传给模型，结果是一个 AIMessage 对象，必须手动去取 .content 才能拿到文字
raw_response = llm.invoke(formatted_text)
print(f"原始方法得到的结果: {raw_response.content}\n")


print("👉 2. 见证奇迹的时刻：LCEL (LangChain 表达式语言)")
# 官网里那些吓人的 `|` 符号，其实非常简单，它就是“工厂流水线”的意思！
# 数据从左边进去，经过一道道工序，从右边出来。
# 这里我们引入了 StrOutputParser (字符串输出解析器)，它的唯一作用就是自动帮你提取 .content

# 组装一条名叫 chain (链条) 的流水线：
# 组装变量 -> 发给大模型 -> 剥离出干净的纯文本
chain = prompt | llm | StrOutputParser()

# 现在，我们不再需要手动去 .format，也不需要手动去 .content
# 直接把变量组成的字典丢进去，流水线自动一气呵成！
lcel_response = chain.invoke({"language": "Java"})
print(f"LCEL 流水线得到的结果: {lcel_response}\n")

print("✅ 第二关执行完毕！")
