a=1
while a <=10:
    print(a)
    a+=1

prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "
    


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
