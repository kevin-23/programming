'''
El polimorfismo permite invocar un método o un
atributo que tiene el mismo nombre en dos clases 
pero que realizan diferentes acciones.
'''

# Example 1
class tomato:

    size = 'Small'

    def color(self):
        print('The tomato color is red')

class apple:

    size = 'Big'

    def color(self):
        print('The apple color is green')

iteration = [tomato(), apple()]
for x in iteration:
    x.color()
    print(x.size)

# Example 2
class car:
    def getWheels():
        print('The car has 4 wheels')

class bike:
    def getWheels():
        print('The bike has 2 wheels')

def wheels(x):
    for i in x:
        i.getWheels()

wheels([car, bike])

# Example 3
class athlete:
    
    def __init__(self, name):
        self.name = name
    
    def action(self):
        self.sport = 'I am a athlete'

    def showInfo(self):
        print(f'My name is {self.name} and I {self.sport}')

class person1(athlete):

    def action(self):
        self.sport = 'play soccer'

class person2(athlete):
    
    def action(self):
        self.sport = 'am a runner'
    
people = [person1('Luis'), person2('David')]
for j in people:
    j.action()
    j.showInfo()