sandwich_orders=['meat','vegetable','tomato','fish','pastrami','pastrami','pastrami']
while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')
print(sandwich_orders)
finished_sandwich=[]
while sandwich_orders:
    current=sandwich_orders.pop()
    print(f"we are making {current}")
    finished_sandwich.append(current)
print('--------result---------')
for sand in finished_sandwich:
    print(f"{sand} is made")
