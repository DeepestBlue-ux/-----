from pathlib import Path
import json
user_info={}
user_info['name']=input('name=')
user_info['age']=int(input('age='))
user_info['location']=input('location=')
content=json.dumps(user_info)
path=Path('user_info.json')
path.write_text(content)

