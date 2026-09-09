import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchResults

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

# 2. 从环境变量中静默读取 Key，杜绝任何明文写在代码里
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()

def mask_key(key: str) -> str:
    """仅用于调试时展示脱敏后的 Key，绝不暴露完整敏感信息"""
    if not key or len(key) < 8:
        return "未配置或过短"
    return f"{key[:6]}******{key[-4:]}"

print("=================================================================")
print("🌐 第十七课：生产级低成本 Web Agent (网络请求 + 严格控量)")
print("=================================================================")
print(f"🔒 [安全检查] 当前加载的 Key: {mask_key(DEEPSEEK_API_KEY)}")
print(f"📍 [接口地址] {DEEPSEEK_BASE_URL}\n")


# ==============================================================================
# 🧰 环节 2：打造轻量级、控 Token 的专属工具箱 (Tools)
# ==============================================================================

# 初始化 DuckDuckGo 搜索
ddg_search = DuckDuckGoSearchResults(output_format="json", max_results=2)

@tool
def search_web(query: str) -> str:
    """
    当需要获取最新的互联网资讯、实时新闻或事实信息时调用此工具。
    输入为搜索关键词，返回前 2 条最相关的网页标题和链接。
    """
    print(f"\n🔍 [Tool: 搜索网络] 正在检索: '{query}' (严格限制仅取前 2 条，省 Token)...")
    try:
        raw_results = ddg_search.invoke(query)
        data = json.loads(raw_results)
        
        # 严格过滤，只把 title, snippet, link 提出来，剔除多余字段
        simplified = []
        for item in data[:2]:
            simplified.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", "")[:120], # 摘要也只取前 120 字
                "link": item.get("link", "")
            })
        return json.dumps(simplified, ensure_ascii=False)
    except Exception as e:
        return f"搜索暂不可用或网络超时: {e}"


@tool
def read_web_page(url: str) -> str:
    """
    当你从搜索结果中拿到了具体网页链接，并需要深入阅读该网页详细正文时调用。
    输入为合法的 URL，返回经过降噪与截断的纯文本正文。
    """
    print(f"\n📖 [Tool: 抓取正文] 正在访问并提取: {url} ...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        resp.encoding = resp.apparent_encoding or "utf-8"
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 1. 垃圾标签大扫除：移除脚本、样式、导航、页脚等无关元素
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
            tag.decompose()
            
        text = soup.get_text(separator="\n", strip=True)
        
        # 2. 核心省钱锁：强制截断前 1200 字符！(杜绝动辄上万字的页面撑爆 Context)
        MAX_CHARS = 1200
        truncated_text = text[:MAX_CHARS]
        
        print(f"   ↳ 提取成功！原始字符数: {len(text)}，硬截断保留前 {len(truncated_text)} 字符以控制 Token。")
        return truncated_text
    except Exception as e:
        return f"访问网页失败: {e}"


tools = [search_web, read_web_page]


# ==============================================================================
# 🧪 环节 3：【0 Token 测试】在不耗费任何大模型费用的情况下验证网络层
# ==============================================================================
def run_zero_cost_local_test():
    """纯 Python 测试：不发任何 LLM 请求，确认网络搜索与网页正文抓取正常"""
    print("-----------------------------------------------------------------")
    print("🚀 [Step 1: 零 Token 本地网络层自检]")
    print("-----------------------------------------------------------------")
    test_query = "Python 官方最新发布版本"
    print(f"1. 测试搜索: '{test_query}'")
    search_res = search_web.invoke({"query": test_query})
    print(f"搜索原始结果: {search_res}\n")
    
    # 尝试解析第 1 个链接并抓取正文
    try:
        items = json.loads(search_res)
        if items and "link" in items[0]:
            first_url = items[0]["link"]
            print(f"2. 测试抓取首个链接: {first_url}")
            page_content = read_web_page.invoke({"url": first_url})
            print(f"抓取正文前 200 字预览:\n{page_content[:200]}...\n")
            print("✅ 零 Token 网络自检顺利通过！数据流打通！\n")
            return True
    except Exception as e:
        print(f"⚠️ 解析或抓取测试失败: {e}")
    return False


# ==============================================================================
# 🤖 环节 4：【四重安全锁】装配低消耗 Agent 并执行任务
# ==============================================================================
def run_agent_task(user_query: str):
    # 安全前置拦截：如果用户还没填 Key，友好报错提示，不发无效请求
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        print("❌ [安全阻断] 检测到当前尚未配置真实的 DEEPSEEK_API_KEY！")
        print("👉 请打开同级目录下的 .env 文件，把你的真实 Key 粘贴在 DEEPSEEK_API_KEY= 后面后再试。")
        return

    # 安全锁 1 & 2：限定 max_tokens 与 temperature，杜绝废话发散
    llm = ChatOpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        model="deepseek-chat",
        temperature=0,
        max_tokens=400  # 限制输出最多 400 token
    )

    system_prompt = (
        "你是一个精简高效的 AI 研究员。"
        "回答问题时必须遵循原则："
        "1. 如果不知道最新情况，优先使用 search_web 搜索。"
        "2. 仅在确实需要深入细节时，才调用 read_web_page 阅读网页。"
        "3. 回答必须言简意赅、直奔主题，严格控制字数在 200 字以内，为用户节省 Token。"
    )

    # 用 LangGraph 预置的标准 ReAct 智能体
    agent = create_react_agent(llm, tools, prompt=system_prompt)

    print("-----------------------------------------------------------------")
    print(f"🙋‍♂️ 用户提问: '{user_query}'")
    print("🧠 Agent 开始思考与行动 (安全熔断限制: 最多 4 步迭代)...")
    print("-----------------------------------------------------------------")

    # 安全锁 3：设置 recursion_limit=4，防止陷入死循环疯狂刷 API
    inputs = {"messages": [("user", user_query)]}
    config = {"recursion_limit": 4}

    step_count = 0
    for step in agent.stream(inputs, config=config, stream_mode="values"):
        step_count += 1
        last_msg = step["messages"][-1]
        
        # 仅打印有意义的输出过程
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            for tc in last_msg.tool_calls:
                print(f"👉 [AI 决策] 准备调用工具: {tc['name']}，参数: {tc['args']}")
        elif last_msg.type == "tool":
            print(f"📥 [工具反馈] 获得数据长度: {len(str(last_msg.content))} 字符")
        elif last_msg.type == "ai" and last_msg.content:
            print("\n🏁 [AI 最终答复]:")
            print(last_msg.content)

    print(f"\n✨ 执行完成！总迭代步骤: {step_count} 步 (在安全预算内)。")


# ==============================================================================
# 🎯 主入口：支持选择先跑“0 Token 自检”还是跑“正式 Agent”
# ==============================================================================
if __name__ == "__main__":
    # 先进行 0 Token 网络连通性自检
    print("请选择运行模式：")
    print("1. 【推荐先行】运行 0 Token 网络自检（纯本地测试搜索与抓取，一分钱不花）")
    print("2. 运行完整 Web Agent（需配置好 .env 中的 Key）")
    
    # 默认自动先跑一遍 0 Token 自检，确保网络没有被墙或超时
    choice = "1"
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("未指定参数，默认先执行 [1. 0 Token 网络自检]...")

    if choice == "1":
        run_zero_cost_local_test()
        print("💡 提示：确认网络自检正常后，可在 .env 填入 Key，然后运行: python lesson17_cost_effective_agent.py 2")
    else:
        run_agent_task("DeepSeek 最新开源的周刊或者动态有什么重点？")
