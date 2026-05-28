from pathlib import Path
import json
path=Path('number1.json')
if path.exists():
    b=path.read_text()
    c=json.loads(b)
    print(f"我知道你最喜欢的数字是{c}")
else:
    a=int(input('输入你喜欢的数字'))
    content=json.dumps(a)
    path.write_text(content)
    print("yijingjilu")

