from flask import Flask, jsonify, request

# Almacena el servidor en app
app = Flask(__name__)

# Una lista que tiene información de los usuarios
users = [{'id': 0, 'name': 'nothing'}, 
        {'id': 1, 'name': 'Gina'}, 
        {'id': 2, 'name': 'Johana'}]

# Consultar todos los usuarios creados
@app.route('/users', methods=['GET'])
def allUsers():

    # Flask no permite retornar una lista directamente
    # por lo que toca jsonificar la lista con jsonify
    #
    # Muestra todos los usuarios en formato json
    return jsonify(users)

# Crear un nuevo usuario
@app.route('/createUser', methods=['POST'])
def createUser():
    
    # Almacenar valores del json en una variable
    newUserData = request.json

    # Agregar el nuevo usuario a la lista
    users.append(newUserData)

    # Mostrar todos los usuarios
    return allUsers()
    
# Parámetros para correr el servidor web (Opcional)
app.run(
    host='127.0.0.1',
    port=8080,
    debug=True
)
