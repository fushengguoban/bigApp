# def repeat(times):
#     print(f"[1] 装饰器工厂启动，记住了你要重复的次数: {times}")
#
#     def actual_decorator(func):
#         print(f"[2] 真正的装饰器启动，拿到了你要装饰的函数: {func.__name__}")
#
#         def wrapper(*args, **kwargs):
#             print(f"\n[3] Wrapper 开始疯狂执行 {times} 次！")
#             for i in range(times):
#                 func(*args, **kwargs)
#
#         return wrapper
#
#     return actual_decorator
#
#
# print(">>> 开始解析代码")
#
#
# @repeat(times=3)
# def say_hello(name):
#     print(f"你好啊。{name}")
#
#
# print(">>> 代码解析完毕，准备调用函数")
# say_hello("Android 老鸟")
# from functools import wraps  # 引入官方工具包
#
#
#
# def simple_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         """这是一个普通的包装起"""
#         print("执行前。。。")
#         return func(*args, **kwargs)
#
#     return wrapper
#
#
# @simple_decorator
# def my_important_api():
#     """这是我写了整整三天的核心业务逻辑"""
#     print("核心业务执行中？》》》》")
#
# # ================= 案发现场 =================
# # 我们来查一下这个 API 函数的真实名字和文档注释
# print("函数的真实名字是:", my_important_api.__name__)
# print("函数的文档注释是:", my_important_api.__doc__)
# from six import reraise
#
#
# def normal_discount(price):
#     return price
#
#
# def vip_discount(price):
#     return price * 0.8
#
#
# def holiday_discount(price):
#     return price - 50 if price > 200 else price
#
#
# def checkout(cart_total, discount_strategy):
#     print(f"原价：{cart_total}")
#
#     final_price = discount_strategy(cart_total)
#     print(f"打折后最终价格: {final_price}\n")
#
#
# print("--- 普通用户结账 ---")
# checkout(300, normal_discount)
#
# # VIP 购买，传 VIP 策略函数
# print("--- VIP 用户结账 ---")
# checkout(300, vip_discount)
# # 节假日购买，直接传节假日策略函数
# print("--- 节假日结账 ---")
# checkout(300, holiday_discount)


# import time
# import threading
#
#
# def cpu_heavy_task():
#     count = 0
#     for i in range(20000000):
#         count += 1
#
#
# print("--- 开始测试单线程 (算 2 次) ---")
# start_time = time.time()
# cpu_heavy_task() # 自己算第 1 次
# cpu_heavy_task() # 自己算第 2 次
# print(f"单线程耗时: {time.time() - start_time:.2f} 秒\n")
#
#
# # ================= 场景 2：双线程一起算 =================
# print("--- 开始测试双线程 (2个人同时各算 1 次) ---")
# start_time = time.time()
# # 创建两个线程
# thread1 = threading.Thread(target=cpu_heavy_task)
# thread2 = threading.Thread(target=cpu_heavy_task)
# # 发令枪响，同时开始！
# thread1.start()
# thread2.start()
#
# # 阻塞主线程，等他们俩都跑完
# thread1.join()
# thread2.join()
# print(f"双线程耗时: {time.time() - start_time:.2f} 秒")


# class SmartHome:
#     def turn_on_light(self):
#         return "💡 灯已打开"
#
#     def turn_on_tv(self):
#         return "📺 电视已打开"
#
#     def play_music(self):
#         return "🎵 音乐已播放"
#
#
# home = SmartHome()
#
# ai_command = "turn_on_tv"
#
# if ai_command == "turn_on_light":
#     print(home.turn_on_light())
# elif ai_command == "turn_on_tv":
#     print(home.turn_on_tv())
# # ... 如果有 100 个家电，这里就要写 100 个 elif！
#
# # ================= Python 程序员的上帝写法 (动态反射) =================
# print("\n--- 见证 Python 反射魔法 ---")
#
# # 1. 探测器：检查有没有这个方法？
# if hasattr(home, ai_command):
#     # 2. 提取器：如果有，直接把这个方法（函数实体）抓出来！
#     # 这就叫 反射！通过字符串名字，拿到了真实的代码执行权！
#     action_func = getattr(home, ai_command)
#
#     # 3. 执行器：加个括号，当场执行！
#     result = action_func()
#     print("AI 执行结果:", result)
# else:
#     print("❌ AI 瞎指挥，家里没这个电器！")


def bark(self):
    return "汪汪汪"

# 用type  动态的创造一个 Dog 类
# 参数1  “dog” 是类的名称
# 参数2  （）里面放继承的父类
# 参数3   {}里面放类的属性和方法
DynamicDog = type("Dog", (), {"age": 1, "speak": bark})

my_dog = DynamicDog()

print(f"这条狗的年龄是{my_dog.age}")
print(f"这条狗的叫声：{my_dog.speak()}")

# 3. 查一下这只狗的品种（类型）
print("它的类型是：", type(my_dog))
