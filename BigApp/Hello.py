import os
# 如果运行报错说找不到 openai 模块，请在下方终端（Terminal）运行: pip install openai
from openai import OpenAI

# 1. 初始化客户端
# 这里以 DeepSeek 为例（因为注册方便送额度，且国内网络直连。它的接口完全兼容 OpenAI）
# 申请地址：https://platform.deepseek.com/
# 如果你使用真正的 OpenAI，请将 base_url 删掉，并换成 OpenAI 的 API_KEY
API_KEY = "YOUR_API_KEY_HERE" # ⚠️ 请在这里填入你申请的真实 API Key

try:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.deepseek.com/v1"
    )

    print("正在连接大模型，请稍候...\n")

    # 2. 发起请求
    response = client.chat.completions.create(
        model="deepseek-chat", # 使用的模型名称
        messages=[
            {"role": "system", "content": "你是一个幽默的编程老师。"},
            {"role": "user", "content": "用一句话解释 Python 和 Java 的最大区别，给一个会写 Android 的人听。"}
        ],
        temperature=1.5
    )

    # 3. 打印结果
    answer = response.choices[0].message.content
    print("🤖 AI 回答：")
    print("-" * 40)
    print(answer)
    print("-" * 40)

except Exception as e:
    print(f"❌ 运行失败，错误信息：\n{e}")
    print("\n💡 提示：")
    print("1. 请确保你已经把代码里的 API_KEY 替换成了真实的密钥。")
    print("2. 确保在终端中运行过 'pip install openai' 来安装依赖库。")
