import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

print("🤖 正在从本地硬盘加载离线重排模型，享受秒加载的快感...")

local_model_path = r"F:\AIDemo\models\bge-reranker-base"  # 👈 如果你的路径不一样，请修改这里！

model = HuggingFaceCrossEncoder(model_name=local_model_path)


print("开始偷偷加载PDF了")

loader = PyPDFLoader(f"F:\金通科技文档\sdkapi-v20201022-r20230522\主板API编程手册(20230522).pdf")

pages = loader.load()

total_pages = len(pages)
print(f"✅ 加载成功！这本 PDF 一共有 {total_pages} 页。")


def clean_my_text(raw_text):
    # 第一招：用最简单的 replace 把空格和换行符替换成“无”
    text = raw_text.replace(" ", "").replace("\n", "")
    text = re.sub(r'\d+', '', text)
    return text


# first_page_text = pages[0].page_content
# clean_text = clean_my_text(first_page_text)
# print("\n🔍 给你悄悄看一眼第一页的前 100 个字：")
# print(clean_text[:100])

print("\n🔪 开始启动智能切片机...")

# 2. 实例化菜刀，请仔细阅读这 3 个参数的含义！
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 设定每个肉丁的最大体积（比如最多 500 个字符）
    chunk_overlap=50,  # 【核心精髓】肉丁之间的重叠字数！前一块结尾的 50 个字，会复制到下一块的开头。为什么要这样？为了防止上下文断层！
    separators=["\n\n", "\n", "。", "！", "？", " "]  # 刀法优先级：先按双换行切，再按单换行，再按句号...
)

# 3. 把整本书 (我们第一步拿到的 pages 变量) 扔进切片机！
# 💡 提示：使用 split_documents 方法，它不仅能切文本，还能完美保留那一页的元数据 (页码信息)！
chunks = text_splitter.split_documents(pages)

print(f"✅ 咔嚓！原本的 {len(pages)} 页 PDF，被完美切成了 {len(chunks)} 个独立的肉丁！")
# 5. 我们随便抽查一个肉丁，比如看看第 10 个肉丁（索引是 9）里面装了什么？
print("\n🥩 抽查第 40 个肉丁的纯文本内容：")
print(chunks[40].page_content)

print("\n🔖 检查这个肉丁身上的标签 (Metadata)，看看页码有没有丢？")
print(chunks[40].metadata)

print("\n🧊 正在开启 Chroma 冷库，免费批量算向量...")

# 2. 实例化向量模型
# 💡 提示：填入我们一直用的免费离线开源小模型："all-MiniLM-L6-v2"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. 把所有的肉丁，一股脑速冻灌入向量库！
# 💡 提示：调用 Chroma 极其经典的 from_documents 方法
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model
)
print("✅ 所有 PDF 肉丁已成功入库！因为用的是本地模型，没花你一分钱 API 费用！")

query = "读取内部存储路径的接口是什么？"
results = vectorstore.similarity_search(query, k=50)


print(f"\n🔍 搜索问题：【{query}】")
print(f"🥇 数据库在 1 毫秒内帮你捞出了最相关的答案：")
print(results[0].page_content)
print(f"📖 重点来了！这个答案出自原始 PDF 的第 {results[0].metadata['page'] + 1} 页！")

pair_list = []
for doc in results:
    pair_list.append([query,doc.page_content])

scores = model.score(pair_list)
print("\n⚖️ 裁判打分结果出炉：")
for i in range(len(results)):
    print(f"肉丁 {i+1} (来自第 {results[i].metadata['page'] + 1} 页) 的裁判得分：{scores[i]}")

# 1. 像拉链一样，把“分数”和“肉丁”一对一打包绑在一起
# 打包后长这样： [(0.32, 肉丁1), (0.001, 肉丁2), (0.996, 肉丁30)...]
paired_results = list(zip(scores,results))

# 2. 按照包裹里的第一个元素（也就是分数）进行排序
# reverse=True 代表降序（分数最高的排在最前面）
paired_results.sort(key= lambda x:x[0],reverse=True)
print("\n🏆 经过裁判重新洗牌后的【最终前 3 名】：\n")


for i in range(3):
    best_score = paired_results[i][0]
    best_doc = paired_results[i][1]

    # 顺便教你一个小技巧，{best_score:.4f} 可以只保留 4 位小数，避免出现带 e 的科学计数法
    print(f"第 {i+1} 名 (裁判得分：{best_score:.4f}，来自第 {best_doc.metadata['page'] + 1} 页):")
    print(best_doc.page_content)
    print("-" * 50)
