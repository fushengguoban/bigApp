import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

# 你的 API Key
API_KEY = "sk-4e969c60e870461e8ae5b5aa14f53848"

print("=========================================")
print("🔴 第四关：赋予双手 (Tools & Agents)")
print("=========================================\n")

# 1. 打造工具 (Tools)
# 大模型本身是没法联网的，也不知道现在的天气。
# 在 LangChain 里，我们只需要写一个普通的 Python 函数，加上 @tool 装饰器。
# 【非常重要】：一定要写好三重引号里的注释 (Docstring)！大模型就是靠看这个注释，来决定要不要用这个工具的。
@tool
def get_weather(city: str) -> str:
    """当用户询问某地的天气时，必须调用此工具。你需要传入城市名称。"""
    
    # 在真实应用中，这里应该写 requests.get() 去调用真实的第三方天气 API
    print(f"\n⚙️ [系统后台悄悄运行...] 正在查询 {city} 的天气 API...")
    
    # 这里为了演示，我们写死几个假数据
    if "北京" in city:
        return "晴天，微风，25度，适合出门旅游。"
    elif "重庆" in city:
        return "暴雨，35度，极为闷热，建议待在家里吃火锅。"
    else:
        return "查不到，可能是外星天气。"

# 把所有的工具打包成一个列表。以后你可以往里加 get_stock_price, search_web 等等。
tools = [get_weather]


# 2. 初始化大模型大脑
llm = ChatOpenAI(
    api_key=API_KEY, 
    base_url="https://api.deepseek.com/v1", 
    model="deepseek-chat"
)


# 3 & 4. 创建 Agent (代理) 并运行
# 什么是 Agent？它就是：大模型 + 一堆工具 + 一套自动循环机制
# 在最新版的 LangChain 架构中，官方全面采用了更强大的 langgraph 来构建 Agent。
# 用 create_react_agent 只需要把大脑(llm)和手(tools)传进去，外加一句系统提示词。
system_prompt = "你是一个万能的私人助理。请使用你手头的工具来回答问题。"
agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)


# ----------------- 开始测试 -----------------

print("🧑 我: 嗨，我打算周末去重庆玩，天气怎么样？")

# 这里大模型会自己判断：
# 1. 用户问天气了 -> 2. 去翻工具箱发现有个 get_weather -> 3. 把“重庆”提取出来传给工具
# -> 4. 拿到结果 -> 5. 组织语言回答用户。

# 我们用 .stream 把它思考的每一步（内心戏）都实时打印出来看！
print("\n[🧠 AI 开始思考与调用工具...]")
for step in agent_executor.stream(
    {"messages": [("user", "嗨，我打算周末去重庆玩，天气怎么样？")]}, 
    stream_mode="values"
):
    # step["messages"][-1] 存放了这一步的产出内容（可能是调用工具，也可能是回复用户）
    step["messages"][-1].pretty_print()
print("[🧠 思考结束]\n")

print("✅ 第四关执行完毕！")
