alien_color='red'
if alien_color=='green':
    print('you gained 5 point')
elif alien_color=='red':
    print('you gained 10 point')

if alien_color=='green':
    point=5 
elif alien_color=='yellow':
    point=10 
elif alien_color=='red':
    point=15
print(f"you gained {point} points")

age=23
if age<2:
    A="baby"
elif age<4:
    A="kido"
elif age<13:
    A="child"
elif age<18:
    A="kid"
elif age<65:
    A="man"
else:
    A="elderly"
print(f"he is a {A}")

fruits=['apple','banana','orange']
if 'banana' in fruits:
    print('you really like banana')
if 'orange' in fruits:
    print('you relly like orange')
if 'grage'in fruits:
    print('you really like grape')
if 'melon' in fruits:
    print('you really like lemon')
if 'apple' in fruits:
    print('you really like apple')

available_toppings=['mushrooms','olives','green peppers','pineapple','extre cheese','pepperoni']
requests=['mushrooms','french fries','rxtra cheese']
for request in requests:
    if request in available_toppings:
        print(f'adding {request}')
    if request not in available_toppings:
        print(f"sorry we don't have {request}")
print("\n your pizza is done")