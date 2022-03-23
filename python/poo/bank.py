# Parent class
class bank():

    # Attribute class
    totalTransactions = 0
    totalDeposited = 0
    totalExtracted = 0

    # Constructor
    def __init__(self, name, amount):
        self.name = name
        self.amount = [amount]

    # Methods
    def deposit(self, depositAmount):
        self.totalTransactions += 1
        self.totalDeposited += depositAmount
        self.amount.append(self.amount[0]+depositAmount)
        self.amount.pop(0)
        print(f'You deposited: ${depositAmount}')

    def extract(self, extractAmount):
        self.totalTransactions += 1
        self.totalExtracted += extractAmount
        self.amount.append(self.amount[0]-extractAmount)
        self.amount.pop(0)
        print(f'You extract: ${extractAmount}')

    def showTotal(self):
        print(f'Your bank account has: ${self.amount[0]}')

    def bankInformation(self):
        print(f'Total transactions for the day are: \
{self.totalTransactions}\nThe total deposited today is: \
${self.totalDeposited}\nThe total extracted today is: \
${self.totalExtracted}')

# Child class
class client(bank):

    # Constructor
    def __init__(self, name, amount):
        super().__init__(name, amount)

    # Calling the parent methods
    def deposit(self, depositAmount):
        return super().deposit(depositAmount)

    def extract(self, extractAmount):
        return super().extract(extractAmount)

    def bankInformation(self):
        return super().bankInformation()

# Declaring new objects
client1 = client('James', 5000)

# Using objects methods
x = 0
while x < 5:
    client1.deposit(330)
    x += 1
    if x == 5:
        i = 0
        while i < 3:
            client1.extract(120)
            i += 1

client1.showTotal()
client1.bankInformation()