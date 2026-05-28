from pathlib import Path
import json
def get_user_name(path):
    if path.exists():
        a=path.read_text()
        username=json.loads(a)
        return username
    else:
        return None

def get_new_user(path):
    name=input('请输入名字 ')
    b=json.dumps(name)
    path.write_text(b)
    return name
    
def greet_user():
    path=Path('username1.json')
    username=get_user_name(path)
    if username:
        print(f"{username} welcome back!")
        v=input('is this you?(y/n)')
        if v=='y':
            print(f'have a nice day {username}!')
        else:
            username=get_new_user(path)
            print(f"we will remember you next time {username}!")
    else:
        username=get_new_user(path)
        print(f"we will remember you next time {username}!")

greet_user()