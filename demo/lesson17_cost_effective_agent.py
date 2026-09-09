import os
from pathlib import Path

from dotenv import load_dotenv

from python.lesson17_cost_effective_agent import DEEPSEEK_API_KEY

# ==============================================================================
# 🛡️ 环节 1：API Key 严格脱敏与安全隔离 (业界生产级规范)
# ==============================================================================
# 1. 自动寻找 .env 文件：先看当前脚本目录，再看上一级工程根目录

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

env_paths = [
    current_dir / ".env",
    project_root / ".env",
    project_root.parent / ".env"
]

loaded = False
for p in env_paths:
    if p.exists():
        load_dotenv(dotenv_path=p, override=True)
        loaded = True
        break

# 2. 从环境变量中静默读取 key,杜绝任何明文写在代码里
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()


def mask_key(key: str) -> str:
    """仅用于调试时展示脱敏后的 key,绝不暴露完整敏感信息"""
    if not key or len(key) < 8:
        return "未配置或过短"
    return f"{key[:6]}******${key[-4:]}"

print("=================================================================")
print("🌐 第十七课：生产级低成本 Web Agent (网络请求 + 严格控量)")
print("=================================================================")
print(f"🔒 [安全检查] 当前加载的 Key: {mask_key(DEEPSEEK_API_KEY)}")
print(f"📍 [接口地址] {DEEPSEEK_BASE_URL}\n")

