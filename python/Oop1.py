# class AndroidUser:
#     def __init__(self, name):
#         self.name = name
#         # 约定俗成，变量名前面加一个下划线，代表它是一个“伪私有变量”，告诉别人别直接碰它
#         self._age = 0
from importlib.metadata import files

# # ================= 魔法时刻 =================
# # 这个注解相当于代替了 Java 的 getAge()
# @property
# def age(self):
#     return self._age
#
# # 这个注解相当于代替了 Java 的 setAge(int age)
# @age.setter
# def age(self, value):
#     if not isinstance(value, int):
#         raise ValueError("年龄必须是整数！")
#     if value < 0 or value > 150:
#         raise ValueError("年龄必须在 0 到 150 之间！")
#     self._age = value

#
# # ====== 测试代码 ======
# user = AndroidUser("老王")
#
# # 像访问普通公共变量一样，直接赋值！(底层会自动调用 @age.setter 的逻辑)
# user._age = 18
# print(f"{user.name} 的年龄是: {user._age}")


# class AndroidProject:
#     def __init__(self, name, files_count):
#         self.name = name
#         self.files_count = files_count
#
#     def __str__(self):
#         return 200
#
#     def __len__(self):
#         return self.files_count
#
#
# my_app = AndroidProject("王者荣耀", 10000)
# print(my_app)
#
# size = len(my_app)
# print(f"这个项目的体积大小是：{size}")


# import json
#
# from numpy.f2py.crackfortran import endifs
#
# config_json = {
#     "app_name": "AI_Assistant",
#     "version": "1.0.0",
#     "features": ["Chat", "RAG"]
# }
#
# with open("my_config.json", "w", encoding="utf-8") as f:
#     json.dump(config_json, f, ensure_ascii=False, indent=4)
#     print("写入完成！你看我需要手动写 f.close() 吗？根本不需要！")
#
# with open("my_config.json", "r", encoding="utf-8") as f:
#     loaded_data = json.load(f)
#     print("\n读取出来的版本号是:", loaded_data["version"])
#     print("支持的功能有:", loaded_data["features"][1])


# def safe_divide(a,b):
#     try:
#         print(f"尝试计算: {a} / {b}")
#         result = a/b
#     except ZeroDivisionError as e:
#         print(f"❌ 捕获到除零异常: {e}")
#     except TypeError as e:
#         print(f"❌ 捕获到类型异常，你是不是传了字符串？: {e}")
#     else:
#         # 只有在 try 里面完全没有报错时，才会执行这里！
#         print(f"✅ 计算成功，没有发生任何异常！结果是: {result}")
#     finally:
#         print("不管怎样，finally 永远会执行，用来兜底清理垃圾。\n")
#
# safe_divide(10,2)
#
# safe_divide(10, 0)
#
# safe_divide(10, "2")


import time

# 这是一个装饰器函数（注意它的结构，函数里面嵌套函数）

# def time_logger(func):
#     def wrapper(*args, **kwargs):
#         print(f"[{func.__name__}] 准备开始执行...")
#         start = time.time()
#
#         result = func(*args, **kwargs)
#
#         end = time.time()
#
#         print(f"[{func.__name__}] 执行结束，耗时: {end - start:.2f} 秒\n")
#
#         return result
#
#     return wrapper
#
#
# # 开始见证魔法
# # 子需要加个 @ 就自动给这个函数套上计时逻辑
# @time_logger
# def download_model(model_name):
#     print(f"正在从网上下载 {model_name}...")
#     time.sleep(1.5)
#     return "下载成功"
#
#
# @time_logger
# def calculate_pi():
#     print("正在疯狂的计算圆周率...")
#     time.sleep(0.5)
#
#
# download_model("DeepSeek-7B")
#
# calculate_pi()


# import asyncio
# import time
#
#
# async def request_ai(model_name, wait_seconds):
#     print(f"🚀 开始向 [{model_name}] 发起网络请求...")
#
#     #     asyncio.sleep 模拟非阻塞的网络等待，必须加 await
#     # 相当于 Kotlin 的 delay(wait_seconds)
#     await asyncio.sleep(wait_seconds)
#
#     print(f"✅ [{model_name}] 返回了结果！")
#
#     return f"{model_name} 的数据"
#
#
# async def main():
#     print("====开始并发请求大模型====")
#     start = time.time()
#
#     results = await asyncio.gather(
#         request_ai("DeepSeek", 2),
#         request_ai("OpenAi", 3)
#     )
#
#     end = time.time()
#     print("\n所有请求完成，拿到数据: {results}")
#     print(f"总耗时: {end - start:.2f} 秒")
#
# # 启动挂起函数
# asyncio.run(main())


# import time
#
#
# def fake_chatgpt(prompt):
#     print(f"收到问题：{prompt}，大模型正在思考...\n")
#     time.sleep(1)
#     reply = "其实大模型流式输出的本质，就是一块一块地往外挤牙膏。"
#
#     for char in reply:
#         yield char  # 记住这个词：吐出！
#         time.sleep(0.2)
#
#
# print("=== 同步模式 (Java常见) ===")
#
# print("=== 流式模式 (Python yield) ===")
#
# for word in fake_chatgpt("流式输出的原理是什么？"):
#     print(word, end="", flush=True)
#
# print("\n\n回答完毕！")


# list_a = [1, 2, 3]
# list_b = [1, 2, 3]
#
# print("场景1 - 内容相等(==)吗？ :", list_a == list_b)
# print("场景1 - 是同一个对象(is)吗？ :", list_a is list_b)
#
# num1 = 200
# num2 = 200
#
# print("\n场景2 - 内容相等(==)吗？ :", num1 == num2)
# print("场景2 - 是同一个对象(is)吗？:", num1 is num2)


import copy

original_data = [
    "普通文本", {"user": "老王", "role": "admin"}
]
# 原始数据 original_data: ['普通文本', {'user': '老王', 'role': 'hacker'}]
# 拷贝数据 shallow_copied_data: ['被篡改的文本', {'user': '老王', 'role': 'hacker'}]
shallow_copied_data = copy.deepcopy(original_data)
# shallow_copied_data = original_data.copy()
shallow_copied_data[0] = "被篡改的文本"

shallow_copied_data[1]["role"] = "hacker"

# 见证奇迹的时刻
print("原始数据 original_data:", original_data)
print("拷贝数据 shallow_copied_data:", shallow_copied_data)


def create_counter():
    count = 0
    print("--- 工厂启动，初始化 count = 0 ---")

    def counter_machine():
        # ⚠️ 魔法关键字：nonlocal (非局部变量)
        # 如果没有这一句，Python 会认为下面那句 count += 1 是你想在内部新建一个叫 count 的变量
        # 加上这句，就是告诉 Python："别瞎建，去外面那一层拿那个叫 count 的变量过来给我修改！"
        nonlocal count
        count += 1
        return count

    # 返回的不是一个值，而是把这个内部函数（造好的机器）当做对象返回出去！
    return counter_machine

# ================= 见证奇迹 =================

# 第一步：调用外层函数，拿到那台“计数机器”
my_counter = create_counter()

# 注意看！此时 create_counter() 这个函数明明已经执行完毕、彻底退出了！
# 按理说它里面的 count 变量应该早就随着函数的死掉而销毁了


# 第二步：但当我们不断按这台机器的开关时...
print("第一次调用:", my_counter())
print("第二次调用:", my_counter())
print("第三次调用:", my_counter())

# 甚至我们可以再造一台完全独立的全新机器
print("\n新造一台机器...")
counter_b = create_counter()
print("新机器的第一次调用:", counter_b())