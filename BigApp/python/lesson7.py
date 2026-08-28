import math

# # 这是我瞎编的 3 维向量（假设是大模型 Embedding 接口返回给你的数字）
# vector_diannao = [0.9, 0.1, 0.8]  # "电脑" 的向量
# vector_macbook = [0.8, 0.2, 0.9]  # "MacBook" 的向量
# vector_pingguo = [0.1, 0.9, 0.1]  # "红富士苹果" 的向量
#
#
#
# def calculate_similarity(v1,v2):
#     # 计算分子（点乘）
#     dot_product = sum(a * b for a, b in zip(v1, v2))
#     # 计算分母（两者的模长相乘）
#     magnitude_v1 = math.sqrt(sum(a * a for a in v1))
#     magnitude_v2 = math.sqrt(sum(b * b for b in v2))
#     # 返回相似度得分（越接近 1 说明意思越相近）
#     return dot_product / (magnitude_v1 * magnitude_v2)
#
#
# # ================= 开始 AI 语义搜索 =================
# score1 = calculate_similarity(vector_diannao, vector_macbook)
# print(f"【电脑】和【MacBook】的语义相似度得分: {score1:.4f}")
# score2 = calculate_similarity(vector_diannao, vector_pingguo)
# print(f"【电脑】和【红富士苹果】的语义相似度得分: {score2:.4f}")


import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    api_key="sk-4e969c60e870461e8ae5b5aa14f53848",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

translation_template = PromptTemplate.from_template(
    """
   你是一个极其精通各国语言的顶级翻译官。
   请把你听到的【源语言】文本，极其地道地翻译成【目标语言】。
   
   【目标语言】: {target_language}
   【源语言文本】: {source_text}
   """
)

# ================= 拼装积木并执行 =================
print("正在生成最终给大模型看的完整文字...\n")

final_prompt = translation_template.format(
    target_language="文言文",
    source_text="老板，我今天感冒发烧了，实在起不来，想请一天假。"
)

print(f"--- 组装好的 Prompt 长这样 ---\n{final_prompt}\n---------------------------")
# 2. 把组装好的长文字，丢给大模型去执行 (invoke)！
print("\n正在呼叫大模型...")
response = llm.invoke(final_prompt)

# 大模型返回的是一个对象，它的 .content 属性就是回答的具体文字
print(f"\n🤖 顶级翻译官的回答：\n{response.content}")
