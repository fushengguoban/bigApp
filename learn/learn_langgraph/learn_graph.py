from typing import TypedDict, NotRequired

from pydantic import BaseModel


class TaskState(BaseModel):
    user_query: str
    tool_result: str = None
    final_answer: str = None
    progress: int = 0


def parse_query(state: TaskState):
    print("\n====== 节点1 parse_query 输入状态 ======")
    print(state)

    query = state.user_query
    update = {
        "tool_result": f"已解析问题: {query}",
        "progress": 30
    }

    return update


def call_tool(state: TaskState):
    print("\n====== 节点2 call_tool 输入状态 ======")
    print(state)

    result = f"工具搜索结果：关于『{state.user_query}』的相关知识"
    update = {
        "tool_result": result,
        "progress": 70
    }

    print("------ 节点2 更新字段 ------")
    print(update)

    return update


def generate_answer(state: TaskState):
    print("\n====== 节点3 generate_answer 输入状态 ======")
    print(state)

    answer = f"最终回答：基于工具结果 -> {state.tool_result}"

    update = {
        "final_answer": answer,
        "progress": 100
    }

    print("------ 节点3 更新字段 ------")
    print(update)

    return update


from langgraph.graph import StateGraph

builder = StateGraph(TaskState)

builder.add_node("parse_query", parse_query)
builder.add_node("call_tool", call_tool)
builder.add_node("generate_answer", generate_answer)

builder.set_entry_point("parse_query")
builder.add_edge("parse_query", "call_tool")
builder.add_edge("call_tool", "generate_answer")

graph = builder.compile()

init_state = TaskState(user_query="什么是LangGraph?")

final_state = graph.invoke(init_state)

print(final_state)

