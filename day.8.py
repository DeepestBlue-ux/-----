class dog:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def sit(self):
        print(f"{self.name} is now setting")
    def roll_over(self):
        print(f"{self.name} rolled over")


class restaurant:
    def __init__(self,name,suisine_type):
        self.restaurant_name=name
        self.cuisine_type=suisine_type
        self.numberserved=0
    def serve(self):
        print(f"the {self.restaurant_name} restaurant has served {self.numberserved} people ")
    def serve_update(self,peopelserve):
        self.numberserved=peopelserve
    def increase_number_served(self,heads):
        self.numberserved += heads
        print(f"plus number {self.numberserved}")
        print(f"the new number we served is {self.numberserved}")
    def describe(self):
        print(f"name:{self.restaurant_name}")
        print(f"meal for today {self.cuisine_type}")
    def open(self):
        print(f"{self.restaurant_name} is now open")
    
hdl=restaurant('haidilao','huoguo')
print(hdl.restaurant_name)
print(hdl.cuisine_type)
hdl.describe()
hdl.open()

huang=restaurant('huangmenji','stew')
huai=restaurant('huainanniuroutang','rice noodles')
pancake=restaurant('roujiamo','meet')
huang.describe()
huai.describe()
pancake.describe()

class User:
    def __init__(self,first_name,last_name,perferance,age,education):
      self.first_name=first_name
      self.last_name=last_name
      self.perferance=perferance
      self.age=age
      self.education=education
    def desccribe(self):
        print(f"the person we have is {self.first_name} {self.last_name},age {self.age} the person perfers to{self.perferance},his education background is {self.education}")
wuyifan=User('wu','yifan','singing','34','highcschool')
zhangtian=User('zhang','tian','soccer','16','middle school')
elbit=User('albit','elstine','study physics','70','professor')
wuyifan.desccribe()
zhangtian.desccribe()
elbit.desccribe()

hdl.numberserved=20
hdl.serve()
hdl.serve_update(30)
hdl.increase_number_served(500)