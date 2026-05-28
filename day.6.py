ucf_u=['alice','brain','candace']
cd_u=[]
while ucf_u:
    current=ucf_u.pop()
    print(f"verfying user:{current}")
    cd_u.append(current)

print(f"users below hans been verfied")
for user in cd_u:
    print(user)

reponses={}
polling_active=True
while polling_active:
    name=input('what"s your name?')
    reponse=input("what mountain would you like to climb")
    reponses[name]=reponse
    repeat=input("would you like other to response?(y/n)")
    if repeat=='n':
        polling_active=False
print("-------result--------")
for name,response in reponses.items():
    print(f"{name}would like to go climb{response}.")