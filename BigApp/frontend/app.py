import streamlit as st
import requests
import uuid

# 后端 FastAPI 的地址 (请确保后端已启动)
API_URL = "http://127.0.0.1:8000/api/chat"

# 页面基础设置
st.set_page_config(page_title="BigApp 智能搜索助理", page_icon="🤖")
st.title("🤖 BigApp 企业级搜索助理")
st.markdown("这是我们的第一个前后端分离 AI 应用！它连接了后端的 FastAPI 接口，并具备 `RAG` 私有数据检索能力。")

# 1. 初始化聊天历史记录（保存在 Session State 里，防止页面刷新丢失）
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = str("test_user_123")

# 2. 将历史聊天记录依次画在屏幕上
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. 接收用户的底部输入框
if user_input := st.chat_input("你想问什么？(尝试问问：咱们公司WiFi密码是多少？)"):

    # 立即在前端显示用户的话
    with st.chat_message("user"):
        st.markdown(user_input)
    # 把用户的话存进历史记录
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 展现"AI正在思考"的动效区块
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*(思考中，正在联系后端 Agent 获取答案...)*")

        try:
            # 真正的核心：把用户的问题发送给后端的 FastAPI！
            response = requests.post(API_URL, json={"message": user_input,
                                                    "session_id": st.session_state.session_id})

            if response.status_code == 200:
                answer = response.json().get("reply", "后端返回格式错误")
            else:
                answer = f"后端报错，状态码：{response.status_code}"
        except Exception as e:
            answer = f"⚠️ 无法连接到后端服务器，请确认 FastAPI (端口8000) 是否正在运行！\n\n报错详情: {e}"

        # 拿到答案后，更新屏幕
        message_placeholder.markdown(answer)

    # 把 AI 的回答也存进历史记录
    st.session_state.messages.append({"role": "assistant", "content": answer})
