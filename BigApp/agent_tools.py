import json
from openai import OpenAI

# ================= 1. 初始化 =================
client = OpenAI(
    api_key="YOUR_API_KEY_HERE", # 你的 Key
    base_url="https://api.deepseek.com/v1"
)

# ================= 2. 你的本地方法 =================
# 大模型是没办法联网的，这是你自己写的查天气的代码。
def get_weather(location):
    print(f"\n⚙️ [本地代码执行中...] 正在查询 {location} 的天气...")
    if "北京" in location:
        return "晴天，25度，微风，非常适合户外活动。"
    else:
        return "下大暴雨，不建议出门。"


# ================= 3. 给 AI 的“说明书” (Tool Description) =================
# 必须严格按照这种格式告诉 AI，你手里有什么武器。
tools_description = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息。如果用户问天气，必须调用此函数。", # AI 完全靠这句话决定是否调它
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：北京、深圳",
                    }
                },
                "required": ["location"],
            },
        }
    }
]

# ================= 4. 第一轮测试 =================
user_question = "周末我想去深圳玩，天气怎么样？"
print(f"👨‍💻 用户提问：{user_question}")

messages = [{"role": "user", "content": user_question}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools_description, # 关键点：把说明书扔给 AI
    tool_choice="auto"       # 关键点：告诉 AI，需不需要调工具，你自己看着办！
)

# 获取 AI 的回复消息
ai_message = response.choices[0].message

# 判断 AI 是否决定调用工具？
if ai_message.tool_calls:
    # 说明 AI 认为它自己回答不了，必须调用工具！
    tool_call = ai_message.tool_calls[0]
    func_name = tool_call.function.name
    
    # 极其强大的一点：AI 会自动从用户的话里提取出参数（它知道 location 是“北京”）
    func_args = json.loads(tool_call.function.arguments)
    
    print(f"\n🤖 AI 思考后决定：我不直接瞎编，请帮我执行本地函数 -> {func_name}")
    print(f"🤖 AI 自动提取出来的参数是 -> {func_args}")
    
    # ================= 5. 本地执行并把结果喂回给 AI =================
    if func_name == "get_weather":
        # 我们真正在本地执行这个 Python 函数
        result_data = get_weather(func_args.get("location"))
        
        # 将 AI 刚才的行为加入历史记录
        messages.append(ai_message) 
        # 将函数执行的结果报告给 AI！
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": func_name,
            "content": result_data # 把“晴天，25度”塞进去
        })
        
        print(f"\n[已经把结果返回给 AI，等待 AI 总结...]")
        
        # 拿着结果再去问 AI 一次
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        
        print("\n🤖 AI 最终的回答：")
        print(final_response.choices[0].message.content)
else:
    print("\n🤖 AI 认为不需要调用工具，直接回答了：")
    print(ai_message.content)
