from pathlib import Path
import json
path=Path('user_info.json')
a=path.read_text()
content=json.loads(a)
print(content)