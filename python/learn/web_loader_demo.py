import bs4
from langchain_community.document_loaders import WebBaseLoader

print("1. 正在访问网页并下载 HTML 内容...")
print("   (这个过程就像你用浏览器打开网页一样)")

# SoupStrainer 就像一个“漏勺”或者“过滤器”
# 它告诉爬虫：我们只要网页里 class 是这些名字的内容，其他导航栏、页脚广告全扔掉！
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer}, # 把漏
    # 勺装配到加载器上
)

print("2. 正在清洗网页，提取纯文本...")
# load() 方法会执行真正的抓取动作，返回一个列表。
# 因为我们只传了 1 个网址，所以列表里只有 1 个元素 docs[0]
docs = loader.load()

print("\n================ 解析结果 =================\n")

# docs[0].page_content 里面存的就是干干净净的纯文本内容
text_length = len(docs[0].page_content)
print(f"这篇文章提取出来的纯文本总字数是：{text_length} 字\n")

print("让我们看看文章的前 500 个字符长什么样：\n")
print("-" * 40)
# [:500] 是 Python 的切片语法，意思是“只截取前 500 个字符”
print(docs[0].page_content[:500])
print("-" * 40)
