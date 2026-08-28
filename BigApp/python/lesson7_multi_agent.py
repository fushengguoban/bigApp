import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated

# =====================================================================
# 💡 第七关：多智能体协作 (Multi-Agent StateGraph)
# =====================================================================
# 核心思想：
# 单个大模型就像一个通才，什么都能干一点，但不够精。
# 在真正的企业级应用中，我们会把大模型“分裂”成多个不同性格的专家。
# 比如：一个负责“疯狂输出代码” (Coder)，另一个负责“挑刺审查” (Reviewer)。
# 通过 LangGraph，我们可以定义它们之间如何互相“踢皮球”，直到结果完美为止。

print("=========================================")
print("🎬 开始构建自动化编程团队：Coder & Reviewer")
print("=========================================\n")

# 1. 准备大模型
# (仍然使用表现极佳的 DeepSeek)
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf" 
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# 2. 定义整个图的“大脑记忆区” (State)
# 两个 Agent 在互相沟通时，就像在一个微信群里聊天，
# 这个 AgentState 就是用来记录这个“群聊天记录”的。
class AgentState(TypedDict):
    # `add_messages` 意思是每次有新消息进来，都是追加，而不是覆盖
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------------------
# 3. 创造节点 (Nodes) —— 也就是我们的数字员工
# ---------------------------------------------------------------------

# 员工 A：程序员 (Coder)
def coder_node(state: AgentState):
    print("\n👨‍💻 [Coder 程序员] 正在埋头写代码...")
    messages = state["messages"]
    
    # 给它戴上程序员的面具
    sys_msg = SystemMessage(
        content="你是一个高级 Python 程序员。根据要求写代码，只输出代码和必要的注释，不要废话。"
                "如果 Reviewer 批评了你，请虚心接受并修改你的代码。"
    )
    # 把“人设”和“聊天记录”一起发给大模型
    response = llm.invoke([sys_msg] + messages)
    print(f"   -> Coder 产出了 {len(response.content)} 个字符的代码。")
    
    # 把它写的东西追加进群聊
    return {"messages": [response]}


# 员工 B：审查员 (Reviewer)
def reviewer_node(state: AgentState):
    print("\n🧐 [Reviewer 审查员] 正在戴着放大镜检查代码...")
    messages = state["messages"]
    
    # 给它戴上严苛审查员的面具
    sys_msg = SystemMessage(
        content="你是一个吹毛求疵的代码审查员。检查上一个 Coder 写的代码。\n"
                "1. 如果代码没有致命Bug、包含了必要的注释、且符合要求，请务必在你的回复的**最开头**输出单词 'PASS'。\n"
                "2. 如果发现问题，请严厉指出，并要求重写，绝不许包含 'PASS'。"
    )
    response = llm.invoke([sys_msg] + messages)
    
    if "PASS" in response.content.upper():
         print("   -> Reviewer: 没毛病，给过！✅")
    else:
         print(f"   -> Reviewer: 发现问题，打回重写！❌ (意见: {response.content[:30]}...)")
         
    return {"messages": [response]}


# ---------------------------------------------------------------------
# 4. 制定规则 (Conditional Edges) —— 谁来决定下一步？
# ---------------------------------------------------------------------

# 这是一个裁判函数，用来判断 Reviewer 的意见后，图该怎么走
def should_continue(state: AgentState):
    # 拿出群聊里的最后一条消息（也就是 Reviewer 刚说的话）
    last_message = state["messages"][-1].content
    
    if "PASS" in last_message.upper():
        return END      # 审查通过，流程彻底结束！
    else:
        return "coder"  # 审查不通过，把球踢回给 Coder，让它重新写！


# ---------------------------------------------------------------------
# 5. 编排工作流 (Build Graph) —— 把员工和规则组装起来
# ---------------------------------------------------------------------
workflow = StateGraph(AgentState)

# 录用这两名员工，分配工位
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)

# 制定工作流转路线：
# 任务刚进来 (START)，必须先交给 coder
workflow.add_edge(START, "coder")

# coder 写完，无条件交给 reviewer 检查
workflow.add_edge("coder", "reviewer")

# reviewer 检查完，调用裁判函数，决定是结束 (END) 还是打回给 coder
workflow.add_conditional_edges("reviewer", should_continue)

# 编译生成我们最终的“自动化公司”
app = workflow.compile()


# =====================================================================
# 6. 开始实战演练！
# =====================================================================
if __name__ == "__main__":
    # 模拟老板 (你) 下达需求
    task_description = "用 Python 写一个计算斐波那契数列的函数，要求使用生成器(yield)，并故意在其中漏写一点注释以便触发 Reviewer 批评。"
    print(f"\n📢 老板下发需求: '{task_description}'\n")
    
    inputs = {"messages": [HumanMessage(content=task_description)]}
    
    # 开始运行流。设置 recursion_limit=5 防止 AI 吵架死循环（最多踢皮球5次）
    try:
        final_state = app.invoke(inputs, {"recursion_limit": 5})
        
        print("\n=========================================")
        print("🎉 自动化流程结束！下面是最终被采用的代码：")
        print("=========================================\n")
        
        # 打印倒数第二条消息，因为最后一条是 Reviewer 的 "PASS"
        print(final_state["messages"][-2].content)
    except Exception as e:
        print(f"\n⚠️ 达到最大循环次数或发生错误: {e}")
        print("可能是 Coder 和 Reviewer 吵起来没完没了了，被系统强行终止。")
