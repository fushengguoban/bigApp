from web_chat import prompt

chat_history = []


def chat_with_memory(user_input):
    # 1.拼接历史+问题
    prompt = "你是友好的助手，结合历史对话回答\n"
    for msg in chat_history:
        prompt += f"{msg['role']}: {msg['content']}\n"
    prompt += f"用户：{user_input}"

    # 2.调用LLM
    response = llm.invoke()