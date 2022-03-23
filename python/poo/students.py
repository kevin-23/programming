# Alumn class
class alumn:

    # Constructor
    def __init__(self, name, qualification):
        self.name = name
        self.qualification = qualification

    def printAlumnInformation(self):
        print(f'The alumn name is: {self.name} \
and the qualification is: {self.qualification}')

    def printQualificationResult(self):
        if self.qualification >= 3:
            print(f'The student approved with {self.qualification}')
        elif self.qualification < 3:
            print(f'The student does not approve, the qualification is {self.qualification}')
        else:
            print('Incorrect qualification')

student1 = alumn('Julian', 4)
student1.printAlumnInformation()
student1.printQualificationResult()

student2 = alumn('Kevin', 2)
student2.printAlumnInformation()
student2.printQualificationResult()