import socket
from dotenv import load_dotenv
import os

load_dotenv()


# Define la función para enviar mensaje al cliente
def returnedSignal(client_address, response_msg):
    bytes_to_send = str.encode(response_msg)
    UDPServerSocket.sendto(bytes_to_send, client_address)

# Obtén la configuración de las variables de entorno
localIP = os.getenv("LOCAL_IP")
localPort = int(os.getenv("LOCAL_PORT"))
bufferSize = int(os.getenv("BUFFER_SIZE"))

# Crea un socket de datagrama
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enlaza el socket a la dirección IP y el puerto especificados
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Escucha para recibir datagramas entrantes
while True:

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1][1]
    
    # Llama a la función returnedSignal() para enviar "Hola" al cliente
    client_address = (localIP, address)
    returnedSignal(client_address, response_msg="pepito que vergas te pasa, se quien sos, tu eres: {}".format(address))

    # Construye mensajes para imprimir en la consola
    clientMsg = "Message from Client: {}".format(message)
    clientIP = "Client IP Address: {}".format(address)
    
    # Imprime los mensajes recibidos y la dirección del cliente
    print(clientMsg)
    print(clientIP)
