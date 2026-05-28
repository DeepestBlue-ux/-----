from pathlib import Path
import json
path=Path('number.json')
content=path.read_text()
a=json.loads(content)
print(a)

path=Path('username.json')
content=path.read_text()
a=json.loads(content)
print(a)