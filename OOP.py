class  Hero:
    def __init__(self, name,):
        self.name = name
        self.live = 3
        self.level = 1
    def hello(self):
        print("Привет, я "+ self.name)
froggy = Hero("Лягушка")
pumpking = Hero("Тыква")
print(pumpking.hello())
print(froggy.hello())