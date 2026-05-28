from pathlib import Path
a=False
while a:
    try:
        b=int(input('请输入数字1'))
        c=int(input('请输入数字2'))
    except ValueError:
        print("您输入的不是整数")
        continue
    d=b+c
    print(d)
    e=input('按quit退出')
    if e=='quit':
        a=False

try:
    q=Path('dogs.txt').read_text(encoding='utf=8')
    print(p)
except Exception:
    pass

try:

    p=Path('cats.txt').read_text(encoding='utf=8')
    print(p)
except Exception:
    pass