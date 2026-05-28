users=['admin','simon','mask','tomas','ash']
if users==[]:
    print('we need more users')
else:
    for user in users:
        if user=='admin':
            print(f'hello,{user},would you like to see a status report?')
        else:
            print(f'hello,{user},thanks for logging again')

new_users=['ADmin','SImon','42','zhongqing','hanyang']
list_1=[]
for user in users:
    list_1.append(user.lower())
for new_user in new_users:
    if new_user.lower() not in list_1:
        print(f'the name {new_user} is ok')
    else:
        print(f'sorry the name {new_user} is token') 

numb=[1,2,3,4,5,6,7,8,9]
for num in numb:
    if num==1:
        print('1st')
    elif num==2:
        print('2nd')
    elif num==3:
        print('3rd')
    else:
        print(f'{num}st')

alian_0={'color':'green','point':5}
print(alian_0['color'])
new_point=alian_0['point']
print(f'you just earned {new_point} points')

alian_0['color']='yellow'
print(alian_0)

alian_0['speed']='slow'
hp=alian_0.get('life')
print(hp)

ren={
    'first_name':'chen',
    'last_name':'li',
    'age':21,
    'city':'DT',
}
print(ren)

game={
    'wang':1,
    'zhang':2,
    'zhao':3,
    'sun':4,
    'li':5,
}
print(f"wang's favorite number is {game['wang']}")
for name,number in game.items():
    print(f"{name}'s favorite number is {number}")

for name in game.keys():
    print(name)
for value in game.values():
    print(value)

