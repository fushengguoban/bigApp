import os
# 强制开启国内镜像站
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# 强制定向到 F 盘
os.environ["HF_HOME"] = "F:/AIDemo/hf_cache"

from huggingface_hub import snapshot_download

print("🚀 准备开始下载 BAAI/bge-reranker-base (约 1.1GB)...")
print("提示：如果中途卡住报错，请直接重新运行这个脚本！它支持断点续传！\n")

# 使用 8 线程并发极速下载，并通过 allow_patterns 只下载必需文件
local_dir = snapshot_download(
    repo_id="BAAI/bge-reranker-base",
    max_workers=8,
    resume_download=True,
    allow_patterns=["*.safetensors", "*.json", "*.txt", "*.md"]
)

print(f"\n✅ 下载完美成功！模型已保存至本地缓存！")
