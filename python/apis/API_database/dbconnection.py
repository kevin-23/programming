# Importar librerías necesarias para la conexión
import pymysql

# Establecer conexión con la base de datos
connection = pymysql.connect(host = 'localhost',
        user = 'root',
        password = '123',
        database = 'myCompany'
        )

dbCursor = connection.cursor()

# Validar la conexión con la base de datos
def validateConnection():
    if connection.open == True:
        print('\n~~~ Established connection to the database ~~~\n')
    else:
        print('\n~~~ Unable to establish a connection to the database ~~~\n')

# Validar usuario para procesos internos
def userValidate(usrId):

    # Consulta que se hará en la base de datos
    query = f'SELECT * FROM employees WHERE id = {usrId}'
    
    # Ejectua la consulta en la base de datos
    dbCursor.execute(query)
    
    # Almacenar los datos en una variable
    data = dbCursor.fetchall()
    
    if len(data) == 0:
        return True
    else:
        return False

# Seleccionar un usuario de la base de datos
def selectUser(usrId):
    
    print(usrId)
    query = f'SELECT * FROM employees WHERE id = {usrId}'

    dbCursor.execute(query)

    data = dbCursor.fetchall()

    # Retorna el resultado de la consulta
    if len(data) != 0: 
        return data
    else:
        return '{"id": "No data found with this id"}'

# Crear un nuevo usuario 
def createUser(data):

    query = f'INSERT INTO employees (firstname, lastname, phone)\
values("{data[0]}","{data[1]}",{data[2]})'

    dbCursor.execute(query)
    
    # Aplicar los cambios en la base de datos 
    connection.commit()
    return 'User successfully created'

# Borra a un usuario
def delUser(usrId):
    
    if userValidate(usrId) == False:
        query = f'DELETE FROM employees WHERE id = {usrId}'
    
        dbCursor.execute(query)

        connection.commit()
        return 'User successfully deleted'
    else:
        return 'User does not exist'

validateConnection()