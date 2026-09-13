#######################核心知识点讲解#########################
# 案例一主要讲了RunnableSequence
# 你在 LangChain 里每一次用竖线 | 拼装流水线时，背后默默诞生的那个对象，就是 RunnableSequence！
# 本质：就是把多个组件按顺序像糖葫芦一样串起来的流水线容器。
# 写法：平时直接用管道符 a | b | c 就够了，优雅、简洁、地道
#
#
# RunnablePassthrough 是一个 【透传组件】，它的核心作用是原样传入数据 适合单个入口，单个场景
#
#
#
# 如何碰到负责的任务流程 比如一个入口，多个场景，如智能客服，这个时候就需要智能分流员，先判断用户需求，
# 然后再把对应的任务分配给对应的人员。
#
# RouterChain (路由链)
# 核心部分：1。目标链：多个处理不同场景的Runnable
# 2.路由选择器：通过条件判断或者大模型，匹配对应的目标链。
# 3.默认链。兜底链条。
#
#
# 路由选择器的工作机制：
# 是路由链的大脑，推荐使用 RunnableBranch 实现条件路由，或者大模型驱动路由
# 1.接收任务，2.通过规则匹配目标链，3让对应的链条执行。
#
#
############################################################


import os
from email.policy import default

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableMap, RunnableBranch
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


# sell_point_prompt = PromptTemplate.from_template(
#     template="从以下产品介绍中提取3个核心卖点，简洁列出：{product_intro}"
# )
#
# marketing_prompt = PromptTemplate.from_template(
#     template="针对{target_audience}，结合以下核心卖点，写一段朋友圈营销话术：{sell_points}"
# )
#
# # 多输入多输出线性链
# overall_chain = (
#         RunnableMap({
#             "sell_points": sell_point_prompt | llm | (lambda x: x.content),
#             "target_audience": RunnablePassthrough(),
#         }) | marketing_prompt | llm
# )
#
# input_data = {
#     "product_intro":"这款无线耳机采用蓝牙5.3芯片，连接稳定无延迟...",
#     "target_audience1":"大学生群体（喜欢运动、预算有限、注重性价比）"
# }
#
# result = overall_chain.invoke(input_data)
# print("👉 真实送给大模型的提示词:\n", result.text)
#
# print("营销话术：")
# print(result.content)


order_prompt = ChatPromptTemplate.from_messages([
    {"system", "你是智能客服，负责解答用户的订单问题"},
    {"human", "用户问题：{query}\n 请引导用户提供订单号，并告知查询流程：1.提供订单号，2.系统验证，3.反馈订单状态"}
])

order_chain = order_prompt | llm | StrOutputParser

# 场景2 ，退货流程链
refund_prompt = ChatPromptTemplate.from_messages([
    {"system", "你是智能客服，负责解答用户退货款问题"},
    {"human",
     "用户问题：{query}\n 请说明退款流程：1.申请退款（订单页面点击退款）；2. 等待审核（1-3个工作日）；3. 退款到账（原路返回，3-5个工作日）。如果用户问退款进度，引导提供退款申请单号。"}
])

refund_chain = refund_prompt | llm | StrOutputParser

# 场景3 ，保修政策链
warranty_prompt = ChatPromptTemplate.from_messages([
    {"system", "你是智能客服，负责解答产品保修政策问题。"},
    {"human",
     "用户问题：{query}\n请说明保修政策：本产品保修期限为1年，保修范围包括质量问题（非人为损坏），保修流程：1. 联系客服；2. 提供购买凭证；3. 寄回检测维修。"}
])

warranty_chain = warranty_prompt | llm | StrOutputParser

# 3. 定义路由判断逻辑（大模型解析需求，输出场景标识）
# 路由提示词，让大模型输出标准化的场景名称，用于后续分支匹配

router_prompt = ChatPromptTemplate.from_messages([
    {"system", """
    你是路由选择器，需根据用户问题判断所属场景，仅输出以下标准化标识之一：
- order：订单查询相关（含订单状态、订单号）
- refund：退货款相关（含退款进度、退款申请）
- warranty：保修相关（含维修、售后保障）
- default：以上均不匹配
无需输出任何其他内容，仅返回标识字符串。"""},
    {"human", "用户的问题：{query}"}
])

router_chain = router_prompt | llm | StrOutputParser()

# 4 默认链，（兜底处理）
default_prompt = ChatPromptTemplate.from_messages(
    [
        {"system",
         "你是智能客服。当遇到无法解答的问题时，请礼貌地告知用户你暂时无法处理该问题，并引导用户重新描述具体问题，或提供联系人工客服的方式（工作时间：9:00-18:00）。语气要友善、专业。"},
        {"human", "用户问题：{query}\n请生成合适的回复。"}
    ]
)

default_chain = default_prompt | llm | StrOutputParser()

# 5. 构建完整的路由链，核心 RunnableBranch 实现条件分发
# 逻辑：先通过 router_chain 获取场景标识，再有 RunnableBranch 分发到对应的链条
full_router_chain = RunnableLambda(lambda x: x) | (
    RunnableBranch(
        (lambda x: x["scene"] == "order", order_chain),
        (lambda x: x["scene"] == "refund", refund_chain),
        (lambda x: x["scene"] == "warranty", warranty_chain),
        default_chain
    )
).with_config(run_name="full_router_chain")


# 6.封装调用函数

def process_query(query: str):
    scene = router_chain.invoke(query)
    return full_router_chain.invoke({"query": query, "scene": scene})
