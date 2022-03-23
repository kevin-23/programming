'''
La encapsulación en Python no existe, sin embargo
hay una sitanxis que se utiliza para hacer refer-
encia de que un atributo o un método es público,
protegido o privado.
'''

# Parent class
class person:

    # Constructor
    def __init__(self, name, country, age):

        # Public attribute
        self.name = name

        # Protected attribute
        self._country = country
        
        # Private attribute
        self.__age = age

    # Methods
    def showInformation(self):
        print(f'My name\'s {self.name} \
I\'m from {self._country} \
and I\'m {self.__age} years old')

    def getPrivateAttribute(self):
        print(self.__age)

    def setPrivateAttribute(self, age):
        if type(age) == int:
            if age > 0 and age < 120:
                self.__age = age
                print(f'The new age is: {self.__age}')
            else:
                print('The new age is invalid')
        else: 
            print('The age must be an integer')
    
person1 = person('Luis', 'Colombia', 20)
person1.showInformation()
person1.getPrivateAttribute()
person1.setPrivateAttribute(22)

# print(person1.__age) <-- ERROR
# print(person1._person__age) <-- NO ERROR
# Python renamed the private attribute to _ClassName__attribute