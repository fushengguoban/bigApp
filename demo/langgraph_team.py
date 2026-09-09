from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage, AIMessage, SystemMessage
import operator

from langchain_openai import ChatOpenAI


class TeamState(TypedDict):
    message: Annotated[Sequence[BaseMessage], operator.add]
    next_worker: str


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


def boss_node(state: TeamState):
    print("--- 👨‍💼 老板：正在思考任务分配... ---")
    message = state["message"]

    # 取出用户的原始需求，
    user_input = message[0].content

    #     简单的老板派发逻辑，如果提到特定关键词，就让研究院先上，否则直接让主笔试

    if "研究" in user_input or "资料" in user_input or "分析" in user_input:
        next_worker = "researcher"
        boss_msg = AIMessage(content="这个任务需要先收集资料，交给【研究员】处理。")
    else:
        next_worker = "writer"
        boss_msg = AIMessage(content="这个任务目标明确，直接交给【主笔】开始撰写。")

    print(f"👨‍💼 老板指令：下一步交给 -> {next_worker}")
    # 返回更新后的 State：追加老板的发言，并指定下一个干活的人
    return {"messages": [boss_msg], "next_worker": next_worker}

def researcher_no(state:TeamState):
    """🕵️‍♂️ 研究员节点：负责“搜索”资料，产出大纲"""
    print("--- 🕵️‍♂️ 研究员：收到，正在努力搜集和整理资料... ---")

    sys_msg=SystemMessage(content="你是一个严谨的研究员。请根据对话上下文，列出详细的研究提纲和关键事实/数据。注意：输出要像一份内部资料报告。")

