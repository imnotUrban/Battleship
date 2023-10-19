import socket
from dotenv import load_dotenv
import os
import time
import json
from utils.message import *
from utils.game import *

TOPEX = 5
TOPEY = 5
ENEMY_LIFE = 6


clientStatus = 0   #0 = sin conectar, 1 = ya se ha conectado, 2 = ya eligió modo de juego, 3 = ya puso barcos, 4 = esta jugando

board = createBoard()

def iniciaConexion(serverAddressPort = ("127.0.0.1", 20001), bufferSize = 1024):
    # Crea un socket UDP en el lado del cliente.
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    return UDPClientSocket


def enviaMensaje(mensaje: str, UDPClientSocket, serverAddressPort = ("127.0.0.1", 20001) ):
    
    # Codifica el mensaje en bytes para poder enviarlo a través del socket.
    bytesToSend = str.encode(mensaje)
    
    # Envía el mensaje al servidor utilizando el socket UDP creado.
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    # Espera a recibir una respuesta del servidor.
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = msgFromServer[0].decode(encoding='utf-8', errors='strict')
    data = json.loads(msgFromServer)
    
    
    # Construye un mensaje para imprimir que incluye la respuesta del servidor.
    msg = "Acción: {}, Status: {}".format(data["action"], data["status"])

    # Imprime el mensaje recibido del servidor.
    print(msg)
    
    status = data["status"]
    
    return data
    

def cierraConexion(UDPClientSocket):
    
    print("Conexión terminada")
    



# Dirección y puerto del servidor al que el cliente enviará el mensaje.
serverAddressPort = ("127.0.0.1", 20001)

# Tamaño del búfer para recibir datos del servidor.
bufferSize = 1024





alreadyConnected = False
UDPClientSocket = iniciaConexion()
keepPlaying = True

while(keepPlaying):
    
    if(not alreadyConnected):   
        #print(" s = Seleccionar modo de juego, c = Conectar, a = Atacar, l = Lose[Rendirse], b = Construir barcos, d = Desconectar ")
        print("Para conectarse al servidor, ingrese 'c' ")
        message_c =input(" Ingrese Acción: ")
        message_c = message_c.lower()
        
        if(message_c == "c"):
            alreadyConnected = True
            status = enviaMensaje(messageConnection(), UDPClientSocket)
            if(status["status"] == "1" or status["status"] == 1):
                clientStatus = 1
                print("Conección con el servidor correcta")
            else:
                print(" No se ha podido realizar la conexión con el servidor, puede que esté lleno")
        
        print("  --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - ---   ")
            
            
    
    if(alreadyConnected):
        
        #### Debe elegir dificultad
        if(clientStatus == 1):
            print("MODO DE JUEGO:  ")
            print(" | 1 = partida contra bots    | - |    0 = partida contra otro usuario |" )
            message_c =input(" Ingrese Modo de juego : ")
            if(message_c == "1" or message_c == "0"):
                status = enviaMensaje(messageBots(int(message_c)), UDPClientSocket)
                clientStatus = 2
            else:
                print("COMANDO NO VÁLIDO")
            print("  --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - ---   ")

        if(clientStatus == 2):
            #ACÁ DEBE INDICAR EL INICIO DE PARTIDA
            print(" Si quiere iniciar la partida ingrese: 'b' ")
            keyWord = input(" ¿Iniciar partida?: ")
            pArray = []
            bArray = []
            sArray = []
            if(keyWord == "b"):
                
                alreadyAdded = True
                
                # --------      PATRULLERO ---------------
                                
                # -------- PATRULLERO ---------------
                print("Ingrese las coordenadas donde desea poner el patrullero (1x1 casillas) [Entre 0 y 4]")

                while True:
                    try:
                        pX = int(input("X: "))
                        if 0 <= pX <= 4:
                            break
                        else:
                            print("El número debe estar entre 0 y 4.")
                    except ValueError:
                        print("Por favor, ingrese un número entero válido para X del patrullero.")

                pArray.append(pX)  # Agrega la coordenada X al arreglo

                while True:
                    try:
                        pY = int(input("Y: "))
                        if 0 <= pY <= 4:
                            break
                        else:
                            print("El número debe estar entre 0 y 4.")
                    except ValueError:
                        print("Por favor, ingrese un número entero válido para Y del patrullero.")

                pArray.append(pY)  # Agrega la coordenada Y al arreglo
                pArray.append(0)  # Agrega un 0 ya que la orientación no importa en el patrullero

                
                
                #Agrega los ships a el arreglo del cliente
                
                # ------ BARCO ------
                alreadyAdded = True  # Inicializado a True para entrar en el bucle

                while alreadyAdded:
                    alreadyAdded = False
                    print(" ---------------------------------------------------------------- ")
                    print("Ingrese las coordenadas donde desea poner el barco (1x2 casillas) [Entre 0 y 3]")

                    while True:
                        try:
                            bX = int(input("X: "))
                            if 0 <= bX <= 3:
                                break
                            else:
                                print("El número debe estar entre 0 y 3.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para X del barco.")

                    while True:
                        try:
                            bY = int(input("Y: "))
                            if 0 <= bY <= 3:
                                break
                            else:
                                print("El número debe estar entre 0 y 3.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para Y del barco.")

                    print("Ingrese la orientación en la que quiere poner el barco (0: vertical, 1: horizontal): ")

                    while True:
                        try:
                            bH = int(input("Orientación: "))
                            if bH in (0, 1):
                                break
                            else:
                                print("La orientación debe ser 0 o 1.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para la orientación del barco.")

                    for i in range(2):  # Se encarga de que no se ponga un barco sobre otro
                        if bH == 0:
                            if pArray[0] == bX and pArray[1] == bY + i:
                                alreadyAdded = True
                                print("El barco no puede ser posicionado sobre otra unidad")
                        elif bH == 1:
                            if pArray[0] == bX + i and pArray[1] == bY:
                                alreadyAdded = True
                                print("El barco no puede ser posicionado sobre otra unidad")

                bArray.append(bX)  # Agrega la coordenada X al arreglo
                bArray.append(bY)  # Agrega la coordenada Y al arreglo
                bArray.append(bH)  # Agrega la orientación al arreglo

                # ------ SUBMARINO -------
                alreadyAdded = True  # Inicializado a True para entrar en el bucle

                while alreadyAdded:
                    alreadyAdded = False
                    print(" ---------------------------------------------------------------- ")
                    print("Ingrese las coordenadas donde desea poner el submarino (1x3 casillas) [Entre 0 y 2]")

                    while True:
                        try:
                            sX = int(input("X: "))
                            if 0 <= sX <= 2:
                                break
                            else:
                                print("El número debe estar entre 0 y 2.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para X del submarino.")

                    while True:
                        try:
                            sY = int(input("Y: "))
                            if 0 <= sY <= 2:
                                break
                            else:
                                print("El número debe estar entre 0 y 2.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para Y del submarino.")

                    print("Ingrese la orientación en la que quiere poner el submarino (0: vertical, 1: horizontal): ")

                    while True:
                        try:
                            sH = int(input("Orientación: "))
                            if sH in (0, 1):
                                break
                            else:
                                print("La orientación debe ser 0 o 1.")
                        except ValueError:
                            print("Por favor, ingrese un número entero válido para la orientación del submarino.")

                    for i in range(3):  # Se encarga de que no se ponga un submarino sobre otro
                        if sH == 0:
                            if pArray[0] == sX and (pArray[1] == sY + i or bArray[1] == sY + i):
                                alreadyAdded = True
                                print("El submarino no puede ser posicionado sobre otra unidad")
                        elif sH == 1:
                            if pArray[0] == sX + i and (pArray[1] == sY or bArray[1] == sY):
                                alreadyAdded = True
                                print("El submarino no puede ser posicionado sobre otra unidad")

                sArray.append(sX)  # Agrega la coordenada X al arreglo
                sArray.append(sY)  # Agrega la coordenada Y al arreglo
                sArray.append(sH)  # Agrega la orientación al arreglo


                
                message_c = json.dumps(messageBuild(pArray, bArray, sArray))
                print(message_c)
                status = enviaMensaje(message_c, UDPClientSocket)
                if(status["status"] == 1 or status["status"] == "1"):
                    print("Juego iniciado")
                clientStatus = 3
                
            else:
                print("Debe ingresar 'b' para iniciar la partida: ")
                
                
        if(clientStatus == 3): 
            #TODO: Aca puede atacar, rendirse o desconectarse (aunque lo ultimo es en todos)
            print("--------------------------------------------------------------")
            print("Ingrese Acción")
            print(" Comandos: a = atacar        -         d = desconectar             -          l = rendirse           -          t = consultar turno")
            try:
                command = input("Ingresa comando: ")
                
                #Ataque
                if(command == "a"):
                    x = int(input("x: "))
                    while(x<0 or x>4 or x==""):
                        print("Ingresa coordenada válida")
                        x = int(input("x: "))
                    y = int(input("y: "))
                    while(y<0 or y>4 or y==""):
                        print("Ingresa coordenada válida")
                        y = int(input("y: "))
                    atackarray = []
                    atackarray.append(x)
                    atackarray.append(y)
                    #Envía ataque
                    status = enviaMensaje(json.dumps(messageAtack(atackarray)), UDPClientSocket)
                    if(status["status"] == "1" and status["action"]== "a" or status["status"] == 1 and status["action"]== "a"): #El ataque dió en el blanco
                        ENEMY_LIFE = ENEMY_LIFE -1
                        print("TU ATAQUE LE DIO AL ENEMIGO !!!! ")
                        
                        board = fillBoard(board, atackarray,True)
                        
                    elif(status["status"] == "0" and status["action"]== "a" or status["status"] == 0 and status["action"]== "a"): #El ataque falló
                        board = fillBoard(board, atackarray,False)
                        print("No has dado a ningún objetivo")
                    
                    elif(status["status"] == "0" and status["action"] == "t" or status["status"] == 0 and status["action"] == "t"):
                        print("**** NO ES TU TURNO DE ATACAR ****")
                    
                
                    elif(status["status"] == "1" and status["action"] == "w" or status["status"] == 1 and status["action"] == "w"):
                        print("\n\n\n\n\n\n\n\n")
                        print("**************************************************")
                        print("************      GANASTE LA PARTIDA      ************")
                        print("**************************************************")

                        clientStatus = 2
                        ENEMY_LIFE = 6
                        board = createBoard()
                        #TODO DESCONECTAR
                    elif(status["status"] == "1" and status["action"] == "l" or status["status"] == 1 and status["action"] == "l"):
                        print("\n\n\n\n\n\n\n\n")
                        
                        print("**************************************************")
                        print("************      PERDISTE LA PARTIDA      ************")
                        print("**************************************************")

                        clientStatus = 2
                        ENEMY_LIFE = 6
                        board = createBoard()
                        #TODO DESCONECTAR
                        
                    

                        
                    print("Vidas del enemigo: {}".format(ENEMY_LIFE))
                    drawBoard(board) if clientStatus!=1 else print("")   #Operador ternario
                    
                if(command == "l"):
                    status = enviaMensaje(json.dumps(messageSurrender()), UDPClientSocket)
                    if(status["status"] == "1" or status["status"] == 1):
                        print(" Has perdido la partida ")
                        clientStatus = 2
                        ENEMY_LIFE = 6
                        board = createBoard()
                        print( " \n\n\n\n\n\n\n\n\n\n\n ")
                        print( " devolviendo al menú de conexión ")
                        time.sleep(3)
                        print( " \n\n\n\n\n\n\n\n\n\n\n ")
                    else:
                        print( " No has podido rendirte ya que no había ninguna partida iniciada" )
                if(command == "t"):
                    status = enviaMensaje(json.dumps(messageTurn()), UDPClientSocket)
                    if(status["status"] == "1" or status["status"] == 1):
                        print(" Es tu turno de jugar ")
                    else:
                        print( " No es tu turno de jugar" )

                if(command == "d"):
                    status = enviaMensaje(json.dumps(messageDisconnect()), UDPClientSocket)
                    if(status["status"] == "1" or status["status"] == 1):
                        print(" Desconexión satisfactoria ")
                        clientStatus = 0
                        alreadyConnected = False
                        ENEMY_LIFE = 6
                        board = createBoard()
                        
                    else:
                        print( " No es tu turno de jugar" )
            #Ganaste la partida
            except ValueError:
                print("Ingrese comando válido")
                   
                
                    #TODO MANEJAR LA DESCONECCIÖN DE USUARIIO PORFAA acuerdatee    
            
            

    
    if(message_c == "quit"):
        keepPlaying = False



