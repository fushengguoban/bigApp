import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

# def search_web(query: str) -> str:
#     """当需要获取最新的新闻、比赛结果、或者你不知道的客观事实时，必须调用这个工具来搜索网络。"""
#     print(f"\n🔧 [系统底层执行] 正在全网搜索关键词：{query} ...")
#
#     # 真实场景里，这里你会写几行代码调用 Google Search 或百度 API。
#     url = "https://www.baidu.com/s"
#     params = {"wd": query}
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Language": "zh-CN,zh;q=0.9"
#     }
#
#     try:
#         response = requests.get(url, params=params, headers=headers, timeout=10)
#         response.raise_for_status()  # 如果网络报错直接跳到 except
#
#         #        使用bs4 解析html 代码
#         soup = BeautifulSoup(response.text, "html.parser")
#
#         # 百度的核心搜索，都在一个  id 叫 'content_left' 的 div 里
#         content_left = soup.find('div', id='content_left')
#
#         if content_left:
#             # 简单粗暴：把这个 div 里面的所有标签全扔掉，只保留纯文字
#             # 在 Android 里这相当于把 HTML 强转成 Plain Text
#             raw_text = content_left.get_text(separator="", strip=True)
#
#             final_text = raw_text[:2000]
#             print(f"✅ 成功从百度抓取了 {len(final_text)} 个字符的数据。")
#             return final_text
#         else:
#             return "未能从百度页面解析到有效内容，可能是触发了反爬虫验证码。"
#     except Exception as e:
#         return f"搜索失败，错误信息：{str(e)}"
#
#
# text=search_web("请帮我研究一下昨晚美股英伟达的股价走势，并写个短评。")
# print(f"test:{text}")


from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchResults
import json

# search_web = DuckDuckGoSearchRun() # 这个直接就可以绑定给 LLM 用
#
# # 直接传入关键词进行搜索，拿到合并后的文本摘要
# query = "DeepSeek 最新模型特点"
# result = search_web.invoke(query)
# print("=== 搜索结果文本 ===")
# print(result)


structured_search = DuckDuckGoSearchResults(output_format="json", max_results=5)

raw_results = structured_search.invoke("LangGraph 生产实践")
print("原始字符:",raw_results)

# 解析为python 字典列表
results = json.loads(raw_results)
for item in results:
    print(f"标题: {item.get('title')}")
    print(f"链接: {item.get('link')}")
    print(f"摘要: {item.get('snippet')}\n")

