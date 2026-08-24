import asyncio

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from sqlalchemy.orm import defer
from sympy import true

llm = ChatOpenAI(
    api_key="sk-4e969c60e870461e8ae5b5aa14f53848",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# def add(a: int, b: int) -> int:
#     """Add two integers.
#
#     Args:
#        a: First integer
#        b: Second integer
#     """
#     return a + b
#
#
# def multiply(a: int, b: int) -> int:
#     """Multiply two integers.
#
#     Args:
#         a: First integer
#         b: Second integer
#     """
#     return a * b
#
#
# class add(BaseModel):
#     """Add two integers."""
#     a: int = Field(..., description="First integer")
#     b: int = Field(..., description="Second integer")
#
#
# class multiply(BaseModel):
#     """Multiply two integers."""
#     a: int = Field(..., description="First integer")
#     b: int = Field(..., description="Second integer")
#
#
# tools = [add, multiply]
#
# llm_with_tools = llm.bind_tools(tools)
# query = "what is 3 * 12?"
# response = llm_with_tools.invoke(query)
# print(response)


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain = prompt | llm | parser


async def main():
    async for chunk in chain.astream({"topic": "parrot"}):
        print(chunk, end="|", flush=true)


asyncio.run(main())
