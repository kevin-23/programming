from abc import ABC, abstractmethod
import random, string

# Abstract class
class password(ABC):

    # Attribute class
    password = ''

    # Constructor
    @abstractmethod
    def __init__(self, length):
        self.setLength(length)
    
    # Methods
    @abstractmethod
    def isStrong(self, password):
        if (len(password)) >= 8:
            print(f'The password is strong')
    
    @abstractmethod
    def generatePassword(self):
        uppercase = random.sample(string.ascii_uppercase, 26)
        lowercase = random.sample(string.ascii_lowercase, 26)
        digits = random.sample(string.digits, 10)

        passwd = random.sample(uppercase + lowercase + digits, self.length)
        passwd = ''.join(passwd)
        self.password = passwd
        self.isStrong(self.password)

    @abstractmethod
    def setLength(self, length):
        if length < 8:
            self.length = 8
        else:
            self.length = length

        self.generatePassword()

    def getPassword(self):
        print(f'The new password is: {self.password}')

    def getLength(self):
        print(f'The password length is: {self.length}')

class generatePasswd(password):

    def __init__(self, length):
        super().__init__(length)

    def isStrong(self, password):
        return super().isStrong(password)
    
    def generatePassword(self):
        return super().generatePassword()
    
    def getPassword(self):
        return super().getPassword()
    
    def getLength(self):
        return super().getLength()

    def setLength(self, newLength):
        return super().setLength(newLength)

password1 = generatePasswd(25)
password1.getPassword()
password1.getLength()
password1.setLength(15)
password1.getPassword()
password1.getLength()