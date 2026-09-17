from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

# ================= 1. 初始化 =================
# 创建你的第一个 Python 后端应用 (就像 SpringBoot 的主类)
app = FastAPI()

# 准备好大模型的客户端
client = OpenAI(
    api_key="", # ⚠️ 记得替换为你真实的 Key
    base_url="https://api.deepseek.com/v1"
)

# ================= 2. 定义数据模型 =================
# 定义 Android 端传过来的 Request Body 格式 (相当于 Kotlin 的 Data Class)
class ChatRequest(BaseModel):
    user_message: str

# ================= 3. 编写 API 接口 =================
# 编写一个 POST 接口 (相当于 @PostMapping("/api/chat"))
@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    print(f"\n📱 收到来自客户端的请求，用户说：{request.user_message}")
    
    # 真正去向大模型要答案
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个幽默的 Android 开发大佬，请用通俗简短的话回答问题。"},
            {"role": "user", "content": request.user_message}
        ]
    )
    
    ai_answer = response.choices[0].message.content
    print(f"🤖 AI 回答完毕，准备回传给客户端...")
    
    # 按照标准规范返回给 Android 的 JSON 数据 (Response Body)
    return {
        "code": 200,
        "message": "success",
        "data": ai_answer
    }

# ================= 4. 启动服务器 =================
if __name__ == "__main__":
    print("🚀 后端服务即将启动...")
    print("✨ 请稍后在浏览器中打开: http://127.0.0.1:8000/docs 看惊喜！")
    # 启动服务器，绑定 8000 端口。0.0.0.0 意味着同一局域网下的手机也能访问
    uvicorn.run(app, host="0.0.0.0", port=8000)
