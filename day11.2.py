from pathlib import Path
import json
#使用条件输入
path=Path('username1.json')
if path.exists():
    content=path.read_text(encoding='utf-8')
    a=json.loads(content)
    print(f"欢迎回来{a}")
else:
    b=input("请输入名字 ")
    content=json.dumps(b)
    path.write_text(content,encoding="utf-8")
    print("已经储存你的名字")

print(f"你成功了{a}")