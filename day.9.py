from pathlib import Path
p=Path('test1.txt')
content=p.read_text()
print(content)

a=Path('../test2.txt')
a1=a.read_text()
print(a1)

b=Path('文本文件/test3.txt')
b1=b.read_text()
print(b1)

c=Path('D:/test4.txt')
c1=c.read_text()
print(c1)

d=Path('guest_book.txt')
name=[]
while True:
    a=input('请输入姓名 按quit退出')
    if a=='quit':
        break
    name.append(a)

content='\n'.join(name)
print(content)
