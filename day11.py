from pathlib import Path
import json
num=[1,2,3,4,5,6,7,8,9]
path=Path('number.json')
content=json.dumps(num)
path.write_text(content)

username=input('ming=')
content=json.dumps(username)
path=Path('username.json')
path.write_text(content)

#使用条件输入
path=Path('username1.json')
if path.exists():
    content=path.read_text
    a=json.loads(content)
    print(f"欢迎回来{a}")
else:
    b=input("请输入名字 ")
    content=json.dumps(b)
    path.write_text(b)
    print("已经储存你的名字")

