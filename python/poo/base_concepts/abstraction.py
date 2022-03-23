'''
La abstracción es prohibir la creación de un
nuevo objeto desde una clase padre logrando que la
clase padre sea accedida solo por las clases hijas.

Todas los métodos abstractos de la clase padre
deben ser declarados en la clase hija
'''

# Import the module to abstract the class
from abc import ABC, abstractmethod

# Declaring the parent and abstract class
class person(ABC):

    # Declaring abstract methods
    @abstractmethod
    def isMarried(self):
        pass

    @abstractmethod
    def isWorking(self):
        pass

    @abstractmethod
    def personSize(self):
        pass

    def isOptional(self):
        print('Is optional')

# Child class
class fireman(person):

    # Constructor
    def __init__(self, name):
        self.name = name
        self.gender = 'Male'

    # Call the abstract methods of the parent class
    def isMarried(self):
        married = True
        if married: 
            print (f'{self.name}: I\'m married.')
    
    def isWorking(self):
        print (True)
    
    def personSize(self):
        print (1.75)

# Child class
class teacher(person):

    # Constructor
    def __init__(self, name):
        self.name = name

    # Call the abstract methods of the parent class
    def isMarried(self):
        print ('I don\'t want to get married')
    
    def isWorking(self):
        print (f'{self.name}: Yes, I\'m a teacher')
    
    def personSize(self):
        print (1.66)

# Declaring new objects
fireman1 = fireman('James')
fireman1.isMarried()

teacher1 = teacher('Ana')
teacher1.isWorking()