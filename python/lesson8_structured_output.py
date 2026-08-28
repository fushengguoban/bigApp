import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf"
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)


class CodeReviewResult(BaseModel):
    has_comments: bool = Field(description="代码中是否包含至少一句中文注释？")
    has_loops: bool = Field(description="代码中是否使用了 for 或 while 循环？")

    is_pass: bool = Field(description="只有当 has_comments 为 True 时，才能为 True。否则必须为 False。")
    critical_feedback: str = Field(description="如果不通过，给出10个字以内的毒舌批评。如果通过，输出'完美'。")


strict_reviewer_llm = llm.with_structured_output(
    CodeReviewResult,
    method="function_calling"
)

bad_code ="""
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
"""
print("🧐 严苛的 Reviewer 正在审查 (强迫结构化输出)...")
# 直接调用！注意，返回的 result 就是一个 CodeReviewResult 对象！
result = strict_reviewer_llm.invoke(f"请严格审查这段代码：\n{bad_code}")

# 就像读取 Android 里的对象属性一样丝滑
print("✅ 审查结果已结构化提取！")
print(f"👉 包含注释吗？ : {result.has_comments}")
print(f"👉 包含循环吗？ : {result.has_loops}")
print(f"👉 是否予通过？ : {result.is_pass}")
print(f"👉 毒舌评语    : {result.critical_feedback}")
