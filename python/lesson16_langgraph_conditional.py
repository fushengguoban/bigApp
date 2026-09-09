import os
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

print("======================================================")
print("🌀 LangGraph 进阶：带循环与人工/AI审核的微服务流")
print("======================================================\n")

# ⚠️ 注意：填入你有效的 API Key
API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf" 
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.5
)

# ========================================================
# 第一步：定义全局状态 (State)
# ========================================================
class WorkflowState(TypedDict):
    topic: str          # 原始主题
    draft: str          # 主笔写的草稿
    feedback: str       # 审核员给出的修改意见
    revision_count: int # 记录修改了多少次（防止无限死循环）
    status: str         # 当前状态：PASS 或 REJECT

# ========================================================
# 第二步：定义节点 (Nodes)
# ========================================================

def writer_node(state: WorkflowState):
    print(f"\n✍️ [主笔 Agent] 正在努力码字... (当前修改次数: {state.get('revision_count', 0)})")
    
    topic = state["topic"]
    feedback = state.get("feedback", "")
    
    # 如果有反馈意见，主笔就要根据意见修改；如果没有，就直接写。
    if feedback:
        prompt = f"请根据以下反馈意见修改关于【{topic}】的文章。\n反馈意见：{feedback}\n请直接输出修改后的正文。"
    else:
        prompt = f"请写一篇关于【{topic}】的短文（大概 50 字）。"
        
    response = llm.invoke(prompt)
    
    # 更新黑板：保存草稿，并把修改次数 +1
    current_count = state.get("revision_count", 0)
    return {"draft": response.content, "revision_count": current_count + 1}

def reviewer_node(state: WorkflowState):
    print("🧐 [审核员 Agent] 正在严厉审核草稿...")
    draft = state["draft"]
    
    # 让 AI 扮演一个挑剔的主编
    messages = [
        SystemMessage(content="你是一个严厉的主编。你要检查文章字数是否少于 80 字。如果是，输出 REJECT 并给出修改意见；如果超过 80 字，直接输出 PASS。"),
        HumanMessage(content=f"这是主笔交上来的草稿：\n{draft}\n\n请按这个格式回复：\n[状态]: PASS 或 REJECT\n[意见]: 你的修改要求")
    ]
    response = llm.invoke(messages).content
    
    # 简单解析大模型的输出
    if "PASS" in response:
        print("   ✅ 审核结果：PASS (通过！)")
        return {"status": "PASS", "feedback": ""}
    else:
        print(f"   ❌ 审核结果：REJECT (打回重做！)\n   意见: {response}")
        return {"status": "REJECT", "feedback": response}


# ========================================================
# 第三步：核心难点 —— 定义条件分支路由函数
# ========================================================
def should_continue(state: WorkflowState) -> Literal["to_writer", "to_end"]:
    """这是一个路由裁判，决定下一步去哪"""
    
    # 如果审核通过，结束！
    if state.get("status") == "PASS":
        return "to_end"
    
    # 强制熔断机制：如果改了超过 3 次还是不通过，强制结束，防止大模型死循环烧钱！
    if state.get("revision_count", 0) >= 3:
        print("🛑 [系统裁判] 强制熔断！修改次数达上限，强行终止流水线。")
        return "to_end"
    
    # 否则，打回给主笔重新写
    return "to_writer"


# ========================================================
# 第四步：画图连线
# ========================================================
print("⚙️ 正在组装带循环的图状态机...")
workflow = StateGraph(WorkflowState)

workflow.add_node("Writer", writer_node)
workflow.add_node("Reviewer", reviewer_node)

workflow.add_edge(START, "Writer")
workflow.add_edge("Writer", "Reviewer")

# ✨ 魔法在这里：添加条件连线 (Conditional Edges)
# 意思是：从 Reviewer 节点出来后，交给 should_continue 函数判断，
# 如果返回 "to_writer"，就走到 Writer 节点；返回 "to_end"，就走到 END 节点。
workflow.add_conditional_edges(
    "Reviewer",
    should_continue,
    {
        "to_writer": "Writer",
        "to_end": END
    }
)

app = workflow.compile()
print("✅ 带循环的分支流水线组装完成！\n")

# ========================================================
# 第五步：测试
# ========================================================
user_topic = "人工智能的未来"
print(f"👔 下达任务：写一篇主题为 '{user_topic}' 的文章，审核员要求必须大于 80 字。\n")

try:
    final_state = app.invoke({"topic": user_topic, "revision_count": 0})
    print("\n🎉 最终产出：")
    print("--------------------------------------------------")
    print(final_state["draft"])
    print("--------------------------------------------------")
except Exception as e:
    print(f"\n❌ 运行失败。报错信息: {e}")
    print("👉 提示：记得去代码里修改你的 API Key！")
