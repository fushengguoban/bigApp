import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun

print("======================================================")
print("🌐 启动真实联网 Agent：赋予大模型探索世界的能力")
print("======================================================\n")

# 1. 准备大模型大脑
# ⚠️ 注意：这里必须填入你最新申请的、有效的 API Key！
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf" 
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0  # Agent 执行任务时，最好把温度设为 0，让它严谨一点
)

# 2. 准备工具箱 (Tools)
# 这里我们直接白嫖 LangChain 社区提供的 DuckDuckGo 搜索引擎工具！
# 它可以突破防火墙（在代码里）直接去外网搜集最新资讯。
search_tool = DuckDuckGoSearchRun()

# 我们把工具装进列表。你以后还可以自己写 @tool 加进来（比如发邮件、操作数据库）
tools = [search_tool]

# 3. 初始化 Agent
print("🤖 正在为 Agent 装备联网搜索工具...")
# 我们使用 ZERO_SHOT_REACT_DESCRIPTION 类型，这是最经典、最好懂的 ReAct 逻辑
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # 开启 verbose，能让我们看到 AI 内心的“自言自语”！
    handle_parsing_errors=True # 防止 AI 偶尔输出格式不对导致崩溃
)

# 4. 开始测试！
# 注意：这个问题，如果不联网，由于大模型知识库停留在过去，它是绝对回答不准的！
user_question = "帮我搜索一下：就在刚刚过去的最近一个月，AI 圈子里爆火的 DeepSeek 发布了什么振奋人心的新模型？它有什么特点？"

print(f"\n🙋‍♂️ 用户指令: '{user_question}'\n")
print("🔥 Agent 开始执行任务：(注意看下面 Action 和 Observation 的交锋)\n")

# 调用 Agent 执行
try:
    response = agent.invoke({"input": user_question})
    print("\n✅ 任务完成，最终汇报：")
    print("--------------------------------------------------")
    print(response["output"])
    print("--------------------------------------------------")
except Exception as e:
    print(f"\n❌ 运行失败。报错信息: {e}")
    print("👉 提示：大概率是因为你的 API Key 无效，请记得去代码第 12 行修改哦！")
