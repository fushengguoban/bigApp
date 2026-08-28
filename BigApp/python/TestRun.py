# import time
#
#
# def say_hello(name, greeting="你好"):
#     time.sleep(1)
#     print(f"{greeting},{name}大佬!")
#
#
# say_hello("Android")
# say_hello("老王", greeting="吃了吗")

#
# 导包：导入 FastAPI, OpenAI, Pydantic。
# 写 Data Class：用 BaseModel 写一个接收请求的类（比如里面有个字段叫 crash_log）。
# 写接口：用 @app.post("/analyze") 并在 def 函数里调用大模型。


from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
import uvicorn

# ================= 1. 初始化 =================
# 创建你的第一个 Python 后端应用 (就像 SpringBoot 的主类)
app = FastAPI()

# 准备好大模型的客户端
client = OpenAI(
    api_key="sk-5cbfd7c8f9264c80abdb2fe3bcaa5cbd", # ⚠️ 记得替换为你真实的 Key
    base_url="https://api.deepseek.com/v1"
)


class ChatRequest(BaseModel):
    crash_log: str

    # 编写一个 POST 接口 (相当于 @PostMapping("/analyze"))
@app.post("/analyze")
async def chat_with_ai(request: ChatRequest):
    print(f"\n📱 收到来自客户端的请求，用户说：{request.crash_log}")

    # 真正去向大模型要答案
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "排查系统log 信息"},
            {"role": "user", "content": request.crash_log}
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
