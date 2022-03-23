# Importar librerías
import os
import requests
from datetime import datetime

# Clase notificación
class notification:

    # Variable de clase
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M")

    # Constructor
    def __init__(self, webhook, bot_name, bot_image):
        self.url = webhook
        self.bot_name = bot_name
        self.bot_image = bot_image

    # Enviar reporte en canal de Discord
    def sendAlert(self, content):

        # Variables
        url = self.url

        # Todos los parámetros en https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data = {
            "username": self.bot_name,
            "avatar_url": self.bot_image,
            "content": content
        }

        # Enviar la notificación
        result = requests.post(url, json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(
                result.status_code))

    # Obtener almacenamiento y memoria de una máquina
    def freeStorageAndMemory(self):

        # Variables
        fileSystem = '/dev/sda2'

        totalStorage = os.popen(
            f'df -h | grep {fileSystem} | awk '"{'print $4'}"'').read()
        usedStorage = os.popen(
            f'df -h | grep {fileSystem} | awk '"{'print $3'}"'').read()
        usedStorage = usedStorage[:-2]

        totalMemory = os.popen(
            'free -g | grep Mem: | awk '"{'print $2'}"'').read()
        usedMemory = os.popen(
            'free -g | grep Mem: | awk '"{'print $3'}"'').read()

        # Mensajes de alerta
        storageAlertMessage = f':rotating_light: {fileSystem} Running out of storage on {self.now}\n\
- Total Storage: {totalStorage.strip()}\n- Used Storage: {usedStorage}G'
        memoryAlertMessage = f':rotating_light: Running out of memory on {self.now}\n\
- Total Memory: {totalMemory.strip()}G\n- Used Memory: {usedMemory.strip()}G'

        # Validar la capacidad actúal de los recursos
        if int(usedStorage) >= 60:
            self.sendAlert(storageAlertMessage)
            if int(usedMemory) >= 4:
                self.sendAlert(memoryAlertMessage)

    # Validar estado de la aplicación usando el PID
    def applicationStatus(self):

        # Variables
        pid = 19317
        app = 'openvpn'

        # Proceso para obtener el status del server
        status = os.popen(
            f'ps aux | grep {app} | awk '"'{print $2}'"' | head -1').read()
        status = " ".join(status.split())

        alertMessage = f':rotating_light: The application PID changed {self.now}\n\
- Current PID: {status.strip()}\n- PID Set: {pid}'
        if int(status) != pid:
            self.sendAlert(alertMessage)

resourceBot = notification(
    "Discord webhook",
    "Resources Bot",
    "https://core.telegram.org/file/811140327/1/zlN4goPTupk/9ff2f2f01c4bd1b013"
)
resourceBot.freeStorageAndMemory()

statusBot = notification(
    "Discord webhook",
    "Status Bot",
    "https://cdn1.iconfinder.com/data/icons/network-and-database-6/48/17-Server-512.png"
)
statusBot.applicationStatus()
