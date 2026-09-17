from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = FastAPI()
client = OpenAI(
    api_key="YOUR_API_KEY_HERE", # ⚠️ 记得替换为你真实的 Key
    base_url="https://api.deepseek.com/v1"
)

class ChatRequest(BaseModel):
    user_message: str

# 定义流式接口
@app.post("/api/chat_stream")
async def chat_stream(request: ChatRequest):
    print(f"\n📱 开始处理流式请求：{request.user_message}")
    
    # 核心 1：将大模型的 stream 参数设为 True
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": request.user_message}],
        stream=True  # 👈 这是魔法开关！这会让大模型不再一次性返回，而是像挤牙膏一样一点点返回
    )
    
    # 核心 2：定义一个生成器函数 (Generator)
    # 这非常像 Kotlin 里的 Flow 或者 RxJava 的 Observable。它不会 return 数据，而是 yield (持续吐出) 数据
    def generate():
        for chunk in response:
            # 拿到每次返回的一小块碎片文字
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True) # 在控制台实时打印，让你亲眼看到打字效果
                yield content

    # 核心 3：使用 FastAPI 专用的 StreamingResponse，边生成边发给 Android
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    print("🚀 流式后端启动...")
    print("✨ 请在浏览器中打开: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
