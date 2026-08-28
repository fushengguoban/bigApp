import os
from pydoc import describe

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# 引入强大的 Pydantic 来定义数据结构
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

llm = ChatOpenAI(
    api_key="sk-4e969c60e870461e8ae5b5aa14f53848",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)


class ResumeInfo(BaseModel):
    name: str = Field(description="候选人的姓名")
    age: int = Field(description="候选人的年龄")
    skills: list[str] = Field(description="候选人掌握的技术栈列表")
    is_qualified: bool = Field(description="如果有Java或者Kotlin经验返回true，否则返回false")


parser = PydanticOutputParser(pydantic_object=ResumeInfo)


resume_template = PromptTemplate(
    template="请提取以下简历中的关键信息。\n\n简历文本：{resume_text}\n\n{format_instructions}",
    input_variables=["resume_text"],
    # 把解析器的“强制命令”强行注入到模板的 format_instructions 变量里！
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

raw_resume = "我叫老王，今年 32 岁了。我干了 10 年开发，平时主要用 Java 和 Kotlin，最近在学大模型。"

final_prompt = resume_template.format(resume_text=raw_resume)

print("--- 偷偷篡改后的终极 Prompt 长这样，仔细看它加了什么！ ---")
print(final_prompt)
print("--------------------------------------------------\n")
# ================= 4. 执行并解析 =================
print("正在呼叫大模型，逼迫它返回 JSON...")
# 第一步：拿到原始字符串
response_string = llm.invoke(final_prompt).content
print(f"大模型的原始输出:\n{response_string}\n")
# 第二步：见证奇迹！用 parser 把玄学字符串变成强类型对象
parsed_obj = parser.parse(response_string)
print("--- 解析成功，现在它是纯正的 Python 对象了！ ---")
print("类型:", type(parsed_obj))
print("提取到的名字:", parsed_obj.name)
print("是否符合招人要求:", parsed_obj.is_qualified)

