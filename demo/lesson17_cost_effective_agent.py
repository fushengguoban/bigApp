from pathlib import Path

from dotenv import load_dotenv

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
        load_dotenv(dotenv_path=)