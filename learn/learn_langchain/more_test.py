from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import os


llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.3
)

parser = StrOutputParser()

#### 分类链
prompt1 = PromptTemplate.from_template(
    "请分析以下新闻文本，仅从候选类别【{category_list}】中选择最合适的一个类别输出，禁止任何多余字符：\n{news_text}"
)

category_chain = prompt1 | llm | parser

# 核心事件提取
prompt2 = PromptTemplate.from_template(
    "这是一篇【{category}】类别的新闻。请从正文中提取核心事件与关键细节：\n{news_text}"
)

event_chain = prompt2 | llm | parser

# 生成摘要
prompt3 = PromptTemplate.from_template(
    "根据【{category}】领域的核心事件【{core_event}】，写一段 100 字以内的精炼摘要："
)
summary_chain = prompt3 | llm | parser

overall_chain = (
    RunnablePassthrough()
    .assign(category=category_chain)
    .assign(core_event=event_chain)
    .assign(summary=summary_chain)
)
inputs = {
    "news_text": "北京时间9月14日，某科技公司在秋季新品发布会上推出了搭载自研神经网络芯片的旗舰手机，该芯片算力较上一代提升40%，支持本地离线运行百亿参数大模型。",
    "category_list": "科技, 财经, 娱乐, 体育"
}

result = overall_chain.invoke(inputs)


print("最终完整字典：")
print(f"1. 分类: {result['category']}")
print(f"2. 核心事件: {result['core_event']}")
print(f"3. 摘要: {result['summary']}")
