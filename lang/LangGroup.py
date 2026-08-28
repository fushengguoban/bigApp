from typing import TypedDict, Annotated

from langgraph.graph import add_messages


class AgentState(TypedDict):
    message: Annotated[list, add_messages]

#
# def coder_node(state: AgentState):
#     messages = state["messages"]
#     response = llm.invoke()
#
#     return {"message": [response]}
