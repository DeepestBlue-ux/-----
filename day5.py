favorite_language={'jen':'python',
                   'sarah':'c',
                   'enward':'rust',
                   'phil':'python',
                   }
alians={'asd':'fgh',
        'qwe':'rty',
        'zxc':'vbn'
        }
sky_peo={'mnb':'vcx',
         'lkj':'hgf',
         'poi':'uyt'}
people=[favorite_language,alians,sky_peo]
print(people)


pet1={'type':'dog',
      'owner':'cindy'
      }
pet2={'type':'cat',
      'owner':'eric',
      }
pet3={'type':'parot',
      'owner':'mike',
      }
pets=[pet1,pet2,pet3]
for i in pets:
    print(f"the type is {i['type']},and the owner is {i['owner']}")

favorite_place={'weizheng':'datong',
                'gan':'england',
                'kaixiang':'shanghai'
                }
for k,v in favorite_place.items():
    print(f"{k}'s favorite place is {v}")

game={
    'wang':[1,2,3,4,5],
    'zhang':2,
    'zhao':3,
    'sun':4,
    'li':5,
}
for k,v in game.items():
    print(f"{k}'s favorite numnber is {v}")

cities={'datong':{'country':'china',
                  'peoprality':'3000000',
                  'fact':'my home town'},
        'toyko':{'country':'jypan',
                 'peoprality':'20000000',
                 'fact':'p5'},
        'paris':{'country':'frans',
                 'peoprality':'100000',
                 'fact':'city of humanity'}
        }
for k,v in cities.items():
    print(f"do you know that {k} lies in {v['country']},the populition is {v['peoprality']},and a fun thing about it is{v['fact']}")