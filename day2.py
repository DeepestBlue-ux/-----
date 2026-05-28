bicycles=['terk','cannondale','redline','specialized','honda']
print(bicycles[1],bicycles[-1])
message=f"my first bicycle was a {bicycles[0].title()}"
print(message)
names=['weizheng','gan','kaixiang']
print(names[0].title(),names[1].lower(),names[2].upper())
message2=f"{names[0]} it's a pleasure to play with you"
print(message2)
bicycles[0]='ducati'
print(bicycles)
bicycles.append('sakamato')
print(bicycles)
k=[]
k.append('honda')
k.append('yamaha')
k.append('suzuki')
print(k)
bicycles.insert(3,'lixiang')
print(bicycles)
del bicycles[1]
print(bicycles)
popped_bicycles=bicycles.pop()
print(bicycles)
print(popped_bicycles)
print(f"the lastest bicycle I owned is {popped_bicycles}")
k.remove('yamaha')
print(k)
too_expensive='ducati'
bicycles.remove(too_expensive)
print(bicycles)
print(f"\nA {too_expensive}is too expensive for me")

famous=['nymar','swan','messi']
print(f'{famous} would you like to hanve dinner with me?')

miss='messi'
print(f"I just heard {miss} can make it here")
famous.remove('messi')
famous.append('lalo')
print(f'{famous} would you like to hanve dinner with me?')
famous.insert(0, 'lacan')
famous.append('nysia')
print(f'{famous} would you like to hanve dinner with me?')
print("im so sorry that i can only invite two of you to join with me")
one=famous.pop()
print(f"{one} im so sorry for your time")
two=famous.pop()
print(f"{two} im so sorry for your time")
three=famous.pop()
print(f"{three} im so sorry for your time")
print(f"{famous[0]} you are still in the list")
print(f"{famous[1]} you are still in the list")
del famous[0:2]
print(famous)
print(len(famous))