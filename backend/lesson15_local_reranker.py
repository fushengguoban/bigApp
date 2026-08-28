from langchain_community.cross_encoders import HuggingFaceCrossEncoder

print("🤖 正在从本地硬盘加载离线重排模型，享受秒加载的快感...")

local_model_path = r"F:\AIDemo\models\bge-reranker-base"  # 👈 如果你的路径不一样，请修改这里！

model = HuggingFaceCrossEncoder(model_name=local_model_path)

print("✅ 本地模型秒加载成功！断网也能用！\n")

query = "读取内部存储路径的接口是什么？"

# 我们准备两个候选句子（模拟之前向量库搜出来的肉丁）
# 第一个是那个恶心的“废话目录”
sentence_1 = "2.2.1 读取内部存储路径 ......................... 15"
# 第二个是我们虚构的“真正的正文”
sentence_2 = "调用 get_internal_path() 接口可以读取内部存储路径，返回值为字符串类型。"
# 4. 让重排模型 (裁判) 给它们重新打分！(分数越高，代表越符合用户的问题)
score_1 = model.score([(query, sentence_1)])
score_2 = model.score([(query, sentence_2)])
print(f"裁判给【废话目录】打分：{score_1[0]}")
print(f"裁判给【真正正文】打分：{score_2[0]}")
