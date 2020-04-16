class Human():
    def __init__(self, name, weight):
        print("__init__실행")
        self.name = name
        self.weight = weight

    #def __str__(self):
    #    return "{} (몸무게 {}kg)".format(self.name, self.weight)
    
    def eat(self):
        self.weight += 0.1
        print("{}가 먹어서 {}kg이 되었습니다.").format(self.name, self.weight)

person = Human("사람",60.5)
print(person)