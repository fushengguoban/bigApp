# 第一章，学习LangChain 核心组件
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts.chat import MessagePromptTemplateT
from langchain_core.runnables import RunnableWithMessageHistory
#######################核心知识点讲解#########################
# 1.LLM 与 ChatModel 的区别
# LLM（文本生成模型）接受一段文字，返回一段文字，
# ChatModel 接收一系列对话消息，返回一条对话消息，适合多伦对话场景，
# PromptTemplate：通过参数化设计实现提示词的规范与复用，降低重复开发成本
# FewShotPromptTemplate：通过动态示例选择与批量管理，适配复杂业务场景，提升提示词效率
# OutputParser：将非结构化输出转化为结构化数据，打通大模型输出与后续业务逻辑的衔接
#
#
#
# 2.进阶实操，全量记忆、窗口记忆、摘要记忆
# 全量记忆：完整保存所有对话历史，适用于短对话场景
# 窗口记忆：仅保留最近N轮对话，控制Token消耗
# 摘要记忆：通过LLM生成对话摘要替代完整历史，平衡上下文连贯性与效率
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
#
#
#
#
############################################################


from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os
from langchain_core.output_parsers import StrOutputParser

# from torch.utils.flop_counter import suffixes


# 加载API密钥，
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("DEEPSEEK_BASE_URL").strip()

print(f"🔒 [安全检查] 当前加载的 Key: {API_KEY}----{BASE_URL}")

if not API_KEY:
    raise ValueError("未检测到 API_KEY，请检查 .env 文件是否配置正确")

# 1.初始化对话模型
chat_model = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="deepseek-v4-flash",  # 选择对话模型
    temperature=0.3,  # 随机性：0-1，越小越严谨，越大越有创造力
    max_tokens=200  # 最大生成 tokens 数，避免生成过长内容
)

# # 2.构造对话消息
# # ChatModel 需要接收的是 “消息列表”，每个消息有角色和内容
# messages = [
#     # system消息：给助手设定身份和行为准则，会影响后续所有回复
#     {"role": "system", "content": "你是一个耐心的AI学习助手，回复简洁易懂，适合高校学生理解。"},
#     # user消息：用户的问题
#     {"role": "user", "content": "请用3句话解释什么是LangChain?"}
# ]
#
# # 3.调用模型生成结果
# # 统一调用方法，invoke(),传入消息列表
#
# result = chat_model.invoke(messages)
#
# # 4.输出结果
# print(f"chatModel的回复：{result.content}")


# examples = [
#     {
#         "subject": "python 编程",
#         "method": "核心目标：掌握基础语法和常用库；学习步骤：1. 学习变量、函数等基础语法 2. 实操小项目（如计算器） 3. 学习Pandas、Matplotlib库；注意事项：多动手实操，遇到错误及时调试。"},
#     {
#         "subject": "机器学习",
#         "method": "核心目标：理解基础算法原理和应用场景；学习步骤：1. 复习数学基础（线性代数、概率） 2. 学习经典算法（线性回归、决策树） 3. 用Scikit-learn实操；注意事项：先理解原理，再动手实现，避免死记硬背。"
#     }
# ]
#
# # 2.定义实例模板，告诉模型如何解析
# example_template = """
# 学科：{subject}
# 学习方法：{method}
# """
#
# example_prompt = PromptTemplate(
#     input_variables=["subject", "method"],
#     template=example_template
# )
#
# # 3.定义最终的提示词模板
#
# few_shot_prompt = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     suffix="学科：{new_subject}\n学习方法:",
#     input_variables=["new_subject"]  # 动态参数，用户要查询的新学科
# )
#
# # 4.格式化模板
# formatted_prompt = few_shot_prompt.format(new_subject="LangChain")
# print("少样本提示词：")
# print(formatted_prompt)


# # 创建 StrOutputParser 核心作用，将LLM 返回的AIMessage 对象，转为纯字符串
# parser = StrOutputParser()
#
# # 链式 调用，模型-> 字符串解析
# chain = chat_model | parser
# result = chain.invoke("请简要介绍 LangChain 输出解析层的作用")
#
# print("StrOutputParser 解析后的字符串：")
# print(result)
# print("\n解析结果类型：", type(result))  # str


full_memory_prompt = ChatPromptTemplate.from_messages({
    ("system", "你是友好的对话助手，需要基于完整的的历史对话回答用户消息。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 历史消息占位符
    ("human", "user_input")  # 用户当前输入
})

base_chain = full_memory_prompt | chat_model

# 会话历史存储（内存模式，生产环境可以替代数据库存储）
full_memory_store = {}


# 4.定义会话历史获取函数

def get_full_memory_history(session_id: str) -> BaseChatMessageHistory:
    """根据session_id获取会话历史，不存在则创建新的历史记录"""
    if session_id not in full_memory_store:
        full_memory_store[session_id] = InMemoryChatMessageHistory()

    return full_memory_store[session_id]

#5.构建带全量记忆的对话链条
full_memory_chain = RunnableWithMessageHistory(
    runnable=base_chain,
    get_session_history=get_full_memory_history,
    input_messages_key="user_input",
    history_messages_key="chat_history"
)
