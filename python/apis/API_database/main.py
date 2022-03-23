from flask import Flask, jsonify, request
from dbconnection import selectUser, createUser, delUser

# Almacena al servidor en app
app = Flask(__name__)

# Seleccionar la información de un usuario 
@app.route('/user', methods=['GET'])
def User():
    
    # Obtener el id del usuario a consultar
    usrId = request.args.get('id')

    # Regresar los datos del usuario en formato json
    return jsonify(selectUser(usrId))

# Crear un nuevo usuario
@app.route('/createUser', methods=['POST'])
def newUser():

    # Obtener los valores del nuevo usuario
    newUserData = request.json
    newUserData = list(newUserData.values())
    
    return createUser(newUserData)

# Borrar a un usuario
@app.route('/deleteUser/<id>', methods=['DELETE'])
def deleteUser(id):
    return delUser(id)

# Definir host y puerto del servidor
app.run(host = 'localhost',
        port = 8085,
        debug = True)
