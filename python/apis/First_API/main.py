# Importar Flask
from flask import Flask

# Almacena el servidor en app
app = Flask(__name__)

# Al ingresar a la ruta /helloworld regresa un texto de Hello World!
@app.route('/helloworld')
def helloworld():
    return 'Hello World!'

# Especifíca por qué host y puerto se debe comunicar (Opcional)
app.run(host='localhost', 
        port=8081,
        debug=True)

