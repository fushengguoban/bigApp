from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse # ⚠️ 引入流式响应工具

import uvicorn

# ================= 1. 初始化 =================
# 创建你的第一个 Python 后端应用 (就像 SpringBoot 的主类)
app = FastAPI()


# 2. 定义 Android 传过来的 JSON 数据结构（完美替代 Builder 模式）
class ChatRequest(BaseModel):
    user_name: str
    user_message: str


def fake_deepseek_stream(message:str):
    reply_text = f"你刚才对我说：'{message}'，我正在思考如何回答你..."
    # 模拟大模型一个字一个字往外吐的过程
    for char in reply_text:
        yield char
        time.sleep(0.1) # 模拟网络延迟，0.1秒吐一个字



@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    print(f"\n📱 收到 {request.user_name} 的提问：{request.user_message}")
    print(f"用户姓名：{request.user_name}")
    print(f"用户消息：{request.user_message}")
    return {"status": "success", "reply": f"你好 {request.user_name}，我收到了你的消息！"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
