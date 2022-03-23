import pymysql

#This class contains the connection method to the database
class dbconnection:

    # Constructor
    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    # Establish the connection with the database
    def con(self):
        dbcon = pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password
        )
        return dbcon, dbcon.cursor()

# This class contain the all queries
class queries(dbconnection):

    # Constructor
    def __init__(self, host, port, user, password):
        super().__init__(host, port, user, password)

    # CRUD methods
    def findOneById(self, table, id):

        # Calls the con method of the parent class and
        # Uses the connection and the cursor for queries
        db = super().con()

        # The query is declared
        query = f'SELECT * FROM {table} WHERE id = {id}'

        # Execute the query in the database
        db[1].execute(query)

        # Transforms the data
        data = list(db[1].fetchall()[0])
        print(f'DATABASE: {table}: {data}')

    def findAll(self, table):
        db = super().con()
        query = f'SELECT * FROM {table}'
        db[1].execute(query)
        data = list(db[1].fetchall())
        print(f'DATABASE: {table}: {data}\n')        

    def createMyCompanyUser(self, table, name, password, email):
        db = super().con()
        query = f'INSERT INTO {table} (name, password, email)VALUES("{name}", "{password}", "{email}")'
        db[1].execute(query)
        db[0].commit()
        
    def updateFirstnameById(self, table, firstname, id):
        db = super().con()
        query = f'UPDATE {table} set name = "{firstname}" WHERE id = {id}'
        db[1].execute(query)
        db[0].commit()        

    def deleteOneById(self, table, id):
        db = super().con()
        query = f'DELETE FROM {table} WHERE id = {id}'
        db[1].execute(query)
        db[0].commit()

# Create new connection objects
myDb = queries('localhost', 3306, 'root', '123')
myDb.findOneById('myCompany.users', '85')
myDb.updateFirstnameById('myCompany.users', 'Julian', '87')
myDb.createMyCompanyUser('myCompany.users', 'David', '123david', 'david1@david.com')