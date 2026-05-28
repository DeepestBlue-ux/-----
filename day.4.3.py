favorite_language={'jen':'python',
                   'sarah':'c',
                   'enward':'rust',
                   'phil':'python',
                   }
friend=['phil','sarah']
for name in favorite_language.keys():
    print(f"Hi {name.title()}")
    if name in friend:
        language=favorite_language[name].title()
        print(f"\t{name.title()},I see you love {language}")

for language in set(favorite_language.values()):
    print(language)

structure={'print':'daying',
           '\n':'huanhang',
           'lower()':'quanbuxiaoxie',
           'upper()':'quanbudaxie',
           'sum()':'jiahe',
           }
for i,k in structure.items():
    print(f"{repr(i)[1:-1]} means {k}")