import socket
from dotenv import load_dotenv
import os
from Jugador import Jugador


load_dotenv()

# Define la función para enviar mensaje al cliente
def returnedSignal(client_address, response_msg):
    bytes_to_send = str.encode(response_msg)
    UDPServerSocket.sendto(bytes_to_send, client_address)

class Servidor:

    def __init__(self):
        self.jugadoresConectados = []  # Lista para almacenar jugadores conectados tipo jugador
        self.partidaEnCurso = False    # Un atributo para controlar si hay una partida en curso

    def iniciarPartida(self):
        if not self.partidaEnCurso:
            # Lógica para iniciar una partida
            # Esto podría incluir la creación de una nueva partida, configuración inicial, etc.
            self.partidaEnCurso = True
            print("Partida iniciada")
        else:
            print("Ya hay una partida en curso")

    def finalizarPartida(self):
        if self.partidaEnCurso:
            # Lógica para finalizar una partida
            # Esto podría incluir el cálculo de resultados, limpieza de la partida, etc.
            self.partidaEnCurso = False
            print("Partida finalizada")
        else:
            print("No hay una partida en curso")

# Obtén la configuración de las variables de entorno
localIP = os.getenv("LOCAL_IP")
localPort = int(os.getenv("LOCAL_PORT"))
bufferSize = int(os.getenv("BUFFER_SIZE"))

# Crea un socket de datagrama
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enlaza el socket a la dirección IP y el puerto especificados
UDPServerSocket.bind((localIP, localPort))
print("SERVIDOR LEVANTADO")

# Crear una instancia del servidor
servidor = Servidor()

reqConnection = os.getenv("REQCONNECTION")



# Escucha para recibir datagramas entrantes
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]    # MENSAJE
    address = bytesAddressPair[1][1]   #PUERTO
    clientIp_recv = bytesAddressPair[1][0]  #IP
    
    #TODO: VER SI EL JUGADOR YA ESTÁ "CONECTADO"   -> AGREGARSE A LA LISTA DE JUGADORES
    
    
    
    
    #TODO: SI NO ESTA CONECTADO, HAY QUE VER SI EL MENSAJE QUE ENVÍA SOLICITA CONEXIÓN
    

    # Llama a la función returnedSignal() para enviar un mensaje al cliente
    client_address = (clientIp_recv, address)
    returnedSignal(client_address, response_msg="CLIENTE: {}".format(address))
    # Construye mensajes para imprimir en la consola
    clientMsg = "Message from Client: {}".format(message)
    clientIP = "Client IP Address: {}".format(address)
    
    # Imprime los mensajes recibidos y la dirección del cliente
    print(clientMsg)
    print(clientIp_recv)

    
    
    
    
 