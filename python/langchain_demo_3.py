import json
import re

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from mpmath.libmp.libelefun import machin
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from typing_extensions import Annotated, TypedDict

from typing import Optional, List


llm = ChatOpenAI(
    api_key="sk-4e969c60e870461e8ae5b5aa14f53848",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)


# class ResumeInfo(BaseModel):
#     name: str = Field(description="候选人的姓名")
#     age: None = Field(description="候选人的年龄")
#     skills: list[str] = Field(description="候选人掌握的技术栈列表")
#     is_qualified: bool = Field(description="如果有Java或者Kotlin经验返回true，否则返回false")
#
#
# parser = PydanticOutputParser(pydantic_object=ResumeInfo)
#
# resume_template = PromptTemplate(
#     template="提取简历信息。\n简历文本：{resume_text}\n{format_instructions}",
#     input_variables=["resume_text"],
#     partial_variables={"format_instructions": parser.get_format_instructions()}
# )
#
# raw_resume = "我叫李四，掌握了 Kotlin 和 Flutter。"
# print("=============== 见证 LCEL 魔法 ===============")
#
# # 🚀 极其震撼的一步！用管道符 `|` 把三个孤立的组件强行焊死在一起，组成一条流水线 (Chain)！
# # 逻辑：上游(模板)的输出，自动变成中游(大模型)的输入；中游的输出，自动变成下游(解析器)的输入！
# chain = resume_template | llm | parser
#
# print("正在启动自动流水线...")
# parsed_obj = chain.invoke({"resume_text": raw_resume})
# print("最终直接拿到的，就是完美的 Python 对象：")
# print("姓名:", parsed_obj.name)
# print("技能:", parsed_obj.skills)

# class Joke(BaseModel):
#     """Joke to tell user."""
#     setup: Annotated[str, ..., "The setup of the joke"]
#     punchline: Annotated[str, ..., "The punchline of the joke"]
#     rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]
#
#
# structured_llm = llm.with_structured_output(Joke, method="function_calling")
# joke = structured_llm.invoke("Tell me a joke about cats")
# print(joke.model_dump_json(indent=2))

class Person(BaseModel):
    """Information about a person."""

    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(
        ..., description="The height of the person expressed in meters."
    )


class People(BaseModel):
    """Identifying information about all people in a text."""

    people: List[Person]


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer the user query. Output your answer as JSON that  "
        "matches the given schema: ```json\n{schema}\n```. "
        "Make sure to wrap the answer in ```json and ``` tags",
    ),
    ("human", "{query}"),
]).partial(schema=People.model_json_schema())


# List[dict] 必须是一个字典的集合
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
       text (str): The text containing the JSON content.

    Returns:
       list: A list of extracted JSON strings.
    """
    text = message.content
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")
