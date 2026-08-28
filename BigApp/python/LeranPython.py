name = "Android开发者"
age = 30

if age >= 18:
    print(f"已经成年了{age}---{age + +1}")
else:
    print("还是个小孩子")

user_info = {
    "name": "Android 菜鸟",
    "skills": ["Java", "kotlin", "Python"],
    "is_single": True
}

user_info["age"] = 18
user_info["skills"].insert(1, "C++")
print(f"这位大佬的名字是：{user_info["name"][1]}")

for skill in user_info["skills"]:
    print(f"掌握的技能：{skill}")
