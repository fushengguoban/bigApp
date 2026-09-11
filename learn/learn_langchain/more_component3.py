#######################核心知识点讲解#########################
# 案例一主要讲了RunnableSequence
# 你在 LangChain 里每一次用竖线 | 拼装流水线时，背后默默诞生的那个对象，就是 RunnableSequence！
# 本质：就是把多个组件按顺序像糖葫芦一样串起来的流水线容器。
# 写法：平时直接用管道符 a | b | c 就够了，优雅、简洁、地道
#
#
#
#
#
#
#
#
#
#
############################################################


import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableMap
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.3
)

###################### 案例一：#######################################################
# sell_point_prompt = PromptTemplate(
#     input_variables=["product_intro"],
#     template="请从以下产品介绍中提取3个核心卖点，用简洁的语言列出：{product_intro}"
# )
#
# sell_point_chain = sell_point_prompt | llm
#
# # 4.中间结果结构化
# extract_sell_points = RunnableLambda(
#     lambda msg: {"sell_points": msg.content}
# )
#
# # 5.组件，生成营销话术，
# marketing_prompt = PromptTemplate(
#     input_variables=["sell_points"],
#     template="请根据以下产品核心卖点，写一段吸引消费者的营销话术（适合朋友圈发布）：{sell_points}"
# )
#
# marketing_chain = marketing_prompt | llm
#
# # 6.线性串联
# overall_chain = (
#         sell_point_chain | extract_sell_points | marketing_chain
# )
#
# # 7 执行
# product_intro = """这款无线耳机采用蓝牙5.3芯片，连接稳定无延迟，支持高清通话；续航长达30小时，充电10分钟可使用2小时；机身采用亲肤硅胶材质，佩戴舒适，防水防汗，适合运动使用。"""
#
# result= overall_chain.invoke(product_intro)
#
# print("\n最终营销话术：")
# print(result.content)
###################### 案例一：#######################################################


sell_point_prompt = PromptTemplate.from_template(
    template="从以下产品介绍中提取3个核心卖点，简洁列出：{product_intro}"
)

marketing_prompt = PromptTemplate.from_template(
    template="针对{target_audience}，结合以下核心卖点，写一段朋友圈营销话术：{sell_points}"
)

# 多输入多输出线性链
overall_chain = (
        RunnableMap({
            "sell_points": sell_point_prompt | llm | (lambda x: x.content),
            "target_audience": RunnablePassthrough(),
        }) | marketing_prompt | llm
)

input_data = {
    "product_intro":"这款无线耳机采用蓝牙5.3芯片，连接稳定无延迟...",
    "target_audience1":"大学生群体（喜欢运动、预算有限、注重性价比）"
}

result = overall_chain.invoke(input_data)
print("👉 真实送给大模型的提示词:\n", result.text)

print("营销话术：")
print(result.content)