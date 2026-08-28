import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "F:/AIDemo/hf_cache"

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

print("🛒 1. 正在初始化京东级混合商品库...")

# 我们精心伪造的 4 款商品。
# 【关键知识点】：注意看 metadata 字典，我们把绝对不能模糊匹配的硬性指标（价格、分类）单独摘了出来！

products = [
    Document(
        page_content="iPhone 15 Pro Max，搭载 A17 芯片，钛金属机身，高端大气上档次，拿在手里有面子。",
        metadata={"name": "iPhone 15 Pro", "price": 8500, "category": "phone"}
    ),
    Document(
        page_content="红米 Note 12，千元神机，性价比极高，超大电池，适合预算有限的学生党。",
        metadata={"name": "红米 Note 12", "price": 1200, "category": "phone"}
    ),
    Document(
        page_content="诺基亚 105，防摔耐造，能当锤子砸核桃。超大按键，超大声音，大字体，绝不眼花，送给老爷爷老奶奶的最佳礼物。",
        metadata={"name": "诺基亚 105", "price": 150, "category": "phone"}
    ),
    Document(
        page_content="联想拯救者 Y9000P，满血版显卡，电竞级高刷屏，散热极佳，畅玩黑神话悟空。",
        metadata={"name": "联想拯救者", "price": 8999, "category": "laptop"}
    )
]
# 把商品连同 Metadata 一起灌入向量冷库

vectorstore = Chroma.from_documents(
    documents=products,
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

print("✅ 商品库入库完成！\n")

print("2. 启动大模型意图解析器 (LLM Intent Parser)...")


# 1. 定义我们希望大模型输出的 JSON 结构 (大厂里管这叫 Slot Filling 填槽)
class SearchIntent(BaseModel):
    max_price: int = Field(description="用户能接受的最高价格。如果没有提到价格，默认为 999999")
    semantic_query: str = Field(description="剔除价格等硬性条件后，用户真正的核心需求（比如：屏幕大、防摔、送长辈）")


API_KEY = "sk-7636f4e8e8a44c0cbb2bc8fb2f0fadaf"
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# 3. 既然底层接口不可用，我们就造一个“输出解析器”，把它自动生成一长串强制 JSON 的提示词
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

parser = PydanticOutputParser(pydantic_object=SearchIntent)

prompt = PromptTemplate(
    template="你是一个严谨的导购员。请提取用户需求，并严格按以下 JSON 格式输出：\n{format_instructions}\n\n【警告】你必须直接输出真实的 JSON 数据，绝对不要输出 Schema 定义！\n例如：\n{{\"max_price\": 1000, \"semantic_query\": \"防水手机\"}}\n\n用户提问：{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# 4. 把 Prompt、大模型、解析器 串联成一条流水线
chain = prompt | llm | parser

# 5. 模拟极其刁钻的用户提问
user_query = "我想买个高端大气上档次的，有面子的，预算最多30000块钱"
print(f"🙋‍♂️ 用户提问: {user_query}")

# 6. 让大模型去解析！
intent = chain.invoke({"query": user_query})

print(f"\n🧠 魔法时刻！大模型把口语变成了 JSON:")
print(f"   💰 提取出的最高预算: {intent.max_price} 元")
print(f"   🔍 提取出的真正需求: {intent.semantic_query}\n")

print("3. 启动混合检索引擎 (Hybrid Search)...")
print(f"👉 [硬过滤]: 正在无情剔除所有大于 {intent.max_price} 元的商品...")
print(f"👉 [软匹配]: 正在用语义寻找: '{intent.semantic_query}'...\n")

# ================= 混合双打核心代码 =================
# query 是让大模型去找“感觉对的”商品
# filter 是传统数据库的强硬规则 ( $lte 意思是 Less Than or Equal，小于等于 )
results = vectorstore.similarity_search(
    query=intent.semantic_query,
    k=2,
    filter={"price": {"$lte": intent.max_price}}  # 核心：价格必须 <= 提取出的最高预算
)

print("🎯 最终为您推荐的商品:")
if not results:
    print("   ❌ 抱歉，没有找到符合您预算和要求的商品。")
else:
    for i, doc in enumerate(results):
        print(f"   👑 排名 {i + 1}: 【{doc.metadata['name']}】 (标价: {doc.metadata['price']}元)")
        print(f"   卖点: {doc.page_content}\n")
