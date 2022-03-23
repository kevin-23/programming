# Exercise to create a person mold
class person:

    # Class attribute
    species = "Homo sapiens"

    # Constructor with instance attributes
    def __init__(self, name, age, gender, profession):
        self.name = name
        self.age = age
        self.gender = gender
        self.profession = profession 

    # Methods
    def data(self):
        print(f'{self.name}\n{self.age}\n{self.gender}\n{self.species}\n{self.profession}')
    
    def informationText(self):
        print('\n~~~ Personal Information ~~~\n')

# Objects or instances
teacher = person("Kevin", 19, "Male", "Teacher")
teacher.informationText()
teacher.data()

julian = person("Julian", 21, "Male", "IT Support")
julian.informationText()
julian.data()