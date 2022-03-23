'''
La herencia permite la creación de otras clases
(clases hijas) en donde las clases hjias pueden 
heredar los métodos de una clase padre.
'''

# Parent class
class person:

    # Constructor
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    # Calculate if the person is an adult
    def isAdult(self):
        if self.age >= 18:
            print('You\'re an adult')
        else:
            print('You aren\'t an adult')

# Child class
class student(person):

    # Constructor
    def __init__(self, name, age, universityProgramme, gender):
        self.universityProgramme = universityProgramme

        # Call the attributes of the parent class
        super().__init__(name, age, gender)

    # Print student information
    def showStudentInformation(self):
        print(f'You name is {self.name} \
and your age is {self.age} \
and you are studying {self.universityProgramme}')

        # Calls the isAdult method of the parent class
        super().isAdult()

# Child class
class teacher(person):

    # Check the gender of the teacher 
    def isMaleTeacher(self):
        if self.gender == 'Male':
            print('Is a man')
        elif self.gender == 'Female':
            print('Is a women')
        else:
            print('Not specified')

# Creates a new student object
student1 = student('Kevin', 25, 'Systems Engineering', 'Male')
student1.showStudentInformation()

teacher1 = teacher('Kevin', 20, 'Male')
teacher1.isMaleTeacher()