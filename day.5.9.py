available_toppings=['mushrooms','olives','green peppers','pineapple','extre cheese','pepperoni']
prompt=f"\nthe available toppings are {available_toppings}"
prompt += "\nplease choose your meal"
active=True
while active:
    message=input(prompt)
    if message == 'finished':
        active=False
    else:
        if message in available_toppings:
            print(f"alright we added {message}")
        else:
            print(f"sorry we don't have {message}")

a=input('age')
a=int(a)
if a <3:
    print('you are free of charge')
elif a<12:
    print('that will cost 10$')
else:
    print('the tictik is 15$')