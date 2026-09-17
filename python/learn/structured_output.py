import json
from openai import OpenAI
from pydantic import BaseModel, Field

# ================= 1. 定义数据结构 (核心！) =================
# 这完全就相当于 Android (Kotlin) 里的 Data Class！
# 我们定义一个类，规定我们期望从大模型那里拿到什么格式的数据。
class AppReviewAnalysis(BaseModel):
    sentiment: str = Field(description="情感倾向，只能是这三个词之一: positive, negative, neutral")
    score: int = Field(description="用户打分，1到10分")
    core_issues: list[str] = Field(description="从评论中提取出的核心痛点或问题列表")
    is_bug: bool = Field(description="用户是否在反馈程序Bug？")

# ================= 2. 初始化 =================
client = OpenAI(
    api_key="YOUR_API_KEY_HERE", # 你的 Key
    base_url="https://api.deepseek.com/v1"
)

# ================= 3. 模拟一条凌乱的用户评价 =================
user_review = "这个App真是绝了，界面做得很漂亮我很喜欢。但是！在点击购买按钮时总是闪退，而且找客服半天不回话！我真的栓Q了，勉强给个6分及格分吧。"

print(f"👨‍💻 原始用户极其随意的评论：\n「{user_review}」\n")
print("-" * 50)

# ================= 4. 发起请求并强制 JSON 输出 =================
# 我们在 System Prompt 中，直接把我们上面定义的 Data Class 的 Schema (结构描述) 扔给 AI
system_prompt = f"""
你是一个专业的用户评论分析器。
请你仔细阅读用户的评论，并严格输出合法的 JSON 格式。绝对不要输出任何多余的废话。
你的 JSON 必须严格遵守以下结构说明：
{AppReviewAnalysis.model_json_schema()}
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_review}
    ],
    # 核心魔法：告诉大模型，你只能输出 JSON 格式，别给我整别的！
    response_format={"type": "json_object"} 
)

# ================= 5. 解析结果 =================
json_string = response.choices[0].message.content

print("🤖 AI 直接吐出的纯 JSON 字符串：")
print(json_string)
print("-" * 50)

# 像 Android 里用 Gson/Moshi 一样，把 JSON 字符串瞬间反序列化成 Python 对象
try:
    parsed_data = AppReviewAnalysis.model_validate_json(json_string)
    print("✅ 成功反序列化为对象！现在你可以像取属性一样读取它们了：")
    print(f"👉 情感判定: {parsed_data.sentiment}")
    print(f"👉 提取出的分数: {parsed_data.score} 分")
    print(f"👉 是否包含 Bug: {'是的' if parsed_data.is_bug else '没有'}")
    print(f"👉 核心问题列表: {parsed_data.core_issues}")
except Exception as e:
    print(f"❌ JSON 解析失败，AI 乱说话了: {e}")
