# class AndroidDeveloper:
#
#     def __init__(self,name,level):
#         self.name = name
#         self.level= level
#
#     def write_code(self,language):
#         print(f"[{self.level}] 级别的 {self.name} 正在疯狂敲 {language} 代码！")
#
#
# dev = AndroidDeveloper("老王","p7")
# dev.write_code("kotlin")
# dev.level="P8"
# dev.write_code("kotlin")
#
from traceback import print_tb


# files = ["wechat.apk", "readme.txt", "taobao.apk", "logo.png", "tiktok.apk"]
# # ---传统老人写法 --类似Java——————#
# apk_list_1 = []
#
# for f in files:
#     if f.endswith(".apk"):
#         apk_list_1.append(f.upper())
#
# print(f"老实人写法结果: {apk_list_1}")
#
# # Python 大佬的流行写法
# # 语法结构：[ 要放入的元素 for 变量 in 列表 if 过滤条件 ]
# apk_list_2 = [f.upper() for f in files if f.endswith(".apk")]
# print(f"一行流魔法结果: {apk_list_2}")
#
# apk_list_2 = []
# nums = [1, 2, 3, 4, 5, 6]
# for f in nums:
#     if f % 2 == 0:
#         apk_list_2.append(f)
#
# nums_title = [f for f in nums if (f % 2 == 0)]
# print(f"一行流魔法结果: {nums_title}")


# a = 100
# print(a)
#
# a = "Hello Android"
# print(a)
#
# is_running = True
# print(is_running)
#
# is_running = 100
# print(is_running)
#
# my_data = None
# print(my_data)


# user_name = "资深工程师"
# bug_type = "NullPointerException"
# prompt = f'''
# 你是一个非常有经验的 {user_name}.
# 现在你的下属写出一个低级错误：{bug_type}.
# 请你用严厉的语气批评他：
# 1.指出为什么会报 {bug_type}
# 2.告诉他“代码上线必须经过 Review!”
# '''
#
# print(prompt)

# skills_list = ["Java", "Android"]
# print(f"初始化 List:{skills_list}")
#
# skills_list.append("Python")
# print(f"增加后 List:{skills_list}")
#
# skills_list[0]="kotlin"
# print(f"修改后 List:{skills_list}")
#
# config_tuple = ("192.168.1.1",8080)
# print(f"服务器配置 Tuple: {config_tuple}")
#
# ip= config_tuple[0]
# print(f"读取出来的 IP 是: {ip}")
#
# config_tuple[0]="114.114.114.114"

# api_response = {
#     "status": 200,
#     "data": "这是一段AI生成的话"
# }
#
# # 危险动作，如果直接用 api_response["error_msg"],程序会当场崩溃 所以先使用get 获取
# error = api_response.get("error_msg")
# print(f"安全读取不存在的key,结果是:{error}")
#
# # get 还能设置默认值，如果找不到就返回你的默认值。
# timeout = api_response.get("timeout", 500)
# print(f"读取到的超时时间是: {timeout}")
#
# brands_list = ["小米", "华为", "小米", "苹果", "华为", "OPPO"]
# print(f"去重前的列表:{brands_list}")
#
# clean_brands_list = set(brands_list)
# print(f"去重厚的列表：{clean_brands_list}")


# data_list = []
#
# if data_list:
#     print("列表里有数据")
# else:
#     print("列表里是空的")
#
# fruits = ["苹果", "香蕉", "橘子"]
#
# for i, fruit in enumerate(fruits):
#     if i == 0:
#         print(f"冠军水果是：{fruit}")
#     elif i == 1:
#         print(f"亚军水果是：{fruit}")
#
#     else:
#         print(f"季军水果是：{fruit}")

# def login(username, password):
#     if username == "admin" and password == "123":
#         # 这里返回的两个值，其实底层自动打成了一个Tuple
#         return {200, "登录成功"}
#     else:
#         return {403, "密码错误", "额外的错误信息"}
#
#
# code = login("admin", "23")
# print(f"状态码: {code}")
# print(f"服务器消息: {code}")

# logs =["登录A","登录B","登录C","登录D","登录E"]
# # 1. 取前三个 (等同于 logs[0:3])
# print(f"前三个日志: {logs[:3]}")
#
# print(f"最后两个日志：{logs[-2:]}")
#
# print(f"跳跃读取：{logs[::2]}")
#
# text = "ABCDEFG"
# print(f"截取子串: {text[2:5]}") # 打印出 CDE
# # [start : end : step]（起 : 止 : 步长）
# print(f"数据倒序：{text[::-1]}")


# def sum_all(*args):
#     print(f"args 底层其实是个元组: {args}")
#     total = sum(args)  # Python 内置的求和函数
#     return total
#
#
# print(sum_all(1, 2, 3, 4, 5))
#
#
# def build_profile(name, **kwargs):
#     print(f"\nkwargs 底层其实是个字典: {kwargs}")
#     profile = {"name": name}
#     profile.update(kwargs)
#     return profile
# # kwargs 底层其实是个字典: {'lever': '18', 'skill': 'kotlin', 'has_hair': False}
# # {'name': 'Android 大佬'}
#
# # kwargs 底层其实是个字典: {'lever': '18', 'skill': 'kotlin', 'has_hair': False}
# # {'name': 'Android 大佬', 'lever': '18', 'skill': 'kotlin', 'has_hair': False}
#
# user = build_profile("Android 大佬", lever="18", skill="kotlin", has_hair=False)
# print(user)

# users = [
#     {"name": "Java大佬", "age": 35},
#     {"name": "Python新星", "age": 22},
#     {"name": "Android老兵", "age": 28}
# ]
# # sort 方法里面可以传一个 key 参数。
# # 我们用 lambda 告诉它：给我按照字典里的 "age" 字段去排！
# users.sort(key=lambda u: u["age"],reverse=True)
# print("按年龄从小到大排序结果：")
# for u in users:
#     print(f"{u['name']} : {u['age']} 岁")


# 挑战开始：请补全这个函数
def analyze_reviews(*args, **kwargs):
    # 1. 尝试从 kwargs 中安全获取最小字数限制，如果没传，默认就是 5
    min_length = kwargs.get("min_len", 5)

    # 2. 结合列表推导式和 if，把 args 里长度大于等于 min_length 的评价筛选出来
    # 提示：字符串长度可以用 len(text)

    valid_reviews = [r for r in args if len(r) >= min_length]

    # 3. 尝试从 kwargs 中获取是否倒序，如果没有传，默认 False
    is_reverse = kwargs.get("is_reverse", False)
    # 4. 对 valid_reviews 进行排序，按照字符串长度排序 (用 lambda)，并结合 reverse 参数
    valid_reviews.sort(key=len, reverse=is_reverse)

    # 5. 用切片语法，只返回前 2 个评价
    return valid_reviews[:2]
    # ================= 老师的测试代码 (请勿修改) =================
    # 发送了 5 条评价，配置要求：最少字数 8 个字，并且字数从长到短倒序排列！


result = analyze_reviews(
    "好用",
    "这个App简直太棒了，极力推荐！",
    "闪退",
    "功能很全，但偶尔卡顿",
    "一般般吧凑合用",
    min_len=8,
    is_reverse=True
)
print(f"最终筛选出的精品评价：{result}")
