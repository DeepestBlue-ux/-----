cars=['bmw','audi','toyota','subaru']
print("here is the original list:")
print(cars)
print("here is the sorted list")
print(sorted(cars,reverse=True))
print("here is the original list again:")
print(cars)

cars1=['bmw','audi','toyota','subaru']
cars1.reverse()
print(cars1)
print(len(cars1))

place=['xizang','suzhou','nanjing','kelong','mosike']
print(place)
print(sorted(place))
print(place)
print(sorted(place,reverse=True))
place.reverse()
print(place)
place.reverse()
print(place)
place.sort()
print(place)
place.sort(reverse=True)
print(place)
print(len(place))

magicians=["alice","cloud","david","lion"]
for magician in magicians:
 print(f"{magician.title()},that was a wandoerul trick")
 print(f"I cant wait to see your next trick {magician.title()}.\n")