import getpass
import os
from pyexpat.errors import messages

from python.lesson6 import result
from structured_output import system_prompt

os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
#
# model = ChatOpenAI(model="gpt-4")
# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="Hi"),
# ]
#
# model.invoke(messages)

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

result = prompt_template.invoke({"language": "italian", "text": "hi"})
print(result)