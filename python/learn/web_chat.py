# pyrefly: ignore [missing-import]
import streamlit as st
import httpx
from openai import OpenAI

# ================= 页面配置 =================
st.set_page_config(page_title="大模型聊天室", page_icon="🤖")
st.title("🤖 我的第一个 AI Web 应用")

# ================= 初始化客户端 =================
# 使用 @st.cache_resource 装饰器，确保每次刷新页面或打字时，不会重复初始化
@st.cache_resource
def get_client():
    return OpenAI(
        api_key="YOUR_API_KEY_HERE", # 更新为你充值后的最新 KEY
        base_url="https://api.deepseek.com/v1"
    )

client = get_client()

# ================= 状态管理 (记忆) =================
# Streamlit 每次交互都会从上到下重新运行代码
# session_state 就像 Android 里的 ViewModel，用来保存哪怕屏幕旋转（页面刷新）也不丢失的数据
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个幽默的编程老师。"}
    ]

# ================= 渲染历史消息 =================
for msg in st.session_state.messages:
    if msg["role"] != "system": # 系统提示词（人设）不用展示在界面上
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ================= 接收输入并请求 AI =================
# st.chat_input 会在页面底部渲染一个极其漂亮的聊天输入框
if prompt := st.chat_input("说点什么吧，比如：Android开发前景如何？"):
    
    # 1. 把用户的提问显示在页面上
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. 把用户提问保存到历史记录中（这就是选项A的本质）
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. 请求大模型，并在页面上展示带有打字机效果的流式回答！
    with st.chat_message("assistant"):
        # 这里发起请求，跟咱们之前的代码一模一样，只是加了 stream=True
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True 
        )
        # st.write_stream 这个神奇的方法会自动处理底层的流式数据，呈现打字机效果
        full_reply = st.write_stream(response)
        
    # 4. 把大模型最终完整的回答也保存到历史记录中
    st.session_state.messages.append({"role": "assistant", "content": full_reply})
