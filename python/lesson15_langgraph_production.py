import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

print("======================================================")
print("🏭 启动大厂生产级流水线：LangGraph 状态机工作流")
print("======================================================\n")

# ⚠️ 注意：填入你有效的 API Key
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf" 
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.7
)

# ========================================================
# 第一步：定义全局共享的“黑板”（State 状态字典）
# 所有的 Agent 都在这块黑板上读写数据
# ========================================================
class TeamState(TypedDict):
    topic: str          # 用户一开始给的主题
    research_data: str  # 研究员查到的资料
    final_article: str  # 主笔写出的最终文章

# ========================================================
# 第二步：定义节点 (Nodes) —— 也就是你的数字员工们
# ========================================================

def researcher_node(state: TeamState):
    """研究员 Agent：负责针对主题生成一些背景资料"""
    print("👨‍🔬 [研究员 Agent] 正在全网检索资料...")
    topic = state["topic"]
    
    # 在真实环境里，这里会调用 DuckDuckGo 搜索。为了演示，我们让大模型直接生成一些“假资料”
    prompt = f"请简要列出关于【{topic}】的3个关键事实，不超过100字。"
    response = llm.invoke(prompt)
    
    # 研究员把查到的资料写在“黑板”上
    return {"research_data": response.content}

def writer_node(state: TeamState):
    """主笔 Agent：负责根据研究员的资料，写出一篇爆款文章"""
    print("✍️ [主笔 Agent] 正在根据资料拼命码字...")
    research_data = state["research_data"]
    
    # 主笔看着黑板上的资料，开始写文章
    messages = [
        SystemMessage(content="你是一个新媒体爆款文章写手。请根据提供的资料，写一段夸张、吸引人的短文。"),
        HumanMessage(content=f"这是研究员给你的资料：\n{research_data}")
    ]
    response = llm.invoke(messages)
    
    # 主笔把写好的文章写在“黑板”上
    return {"final_article": response.content}

# ========================================================
# 第三步：画图连线 (Edges) —— 制定流水线规则
# ========================================================
print("⚙️ 正在组装工业流水线...")
workflow = StateGraph(TeamState)

# 1. 把员工安排到流水线的工位上
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Writer", writer_node)

# 2. 规定流转顺序
workflow.add_edge(START, "Researcher")    # 一开始先让研究员干活
workflow.add_edge("Researcher", "Writer") # 研究员干完，把活交给主笔
workflow.add_edge("Writer", END)          # 主笔干完，流程结束

# 3. 编译整条流水线（生成最终的可执行图）
app = workflow.compile()
print("✅ 流水线组装完成！\n")

# ========================================================
# 第四步：开始执行！
# ========================================================
user_topic = "人类移民火星"
print(f"👔 [老板(你)] 下达任务：给我写一篇关于 '{user_topic}' 的文章。\n")

try:
    # 把初始数据（只包含主题）放进黑板，启动流水线！
    final_state = app.invoke({"topic": user_topic})
    
    print("\n🎉 流水线执行完毕！老板请过目：")
    print("--------------------------------------------------")
    print(final_state["final_article"])
    print("--------------------------------------------------")
    
except Exception as e:
    print(f"\n❌ 运行失败。报错信息: {e}")
    print("👉 提示：如果报 Authentication Fails，记得去代码第 12 行修改你的 API Key！")
