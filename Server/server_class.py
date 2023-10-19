import socket
from dotenv import load_dotenv
import os
from Jugador import Jugador
import json
from utils.message import *
from clases.Bot import Bot
import random


load_dotenv()

# Define la función para enviar mensaje al cliente
def returnedSignal(client_address, response_msg):
    print("MENSAJE DE RESPUESTA OJOOOOO")
    print(response_msg)
    bytes_to_send = str.encode(response_msg)
    UDPServerSocket.sendto(bytes_to_send, client_address)


class Servidor:
    def __init__(self):
        self.jugadoresConectados = []  # Lista para almacenar jugadores conectados tipo jugador
        self.nJugadores = 0
        self.partidaEnCurso = False    # Un atributo para controlar si hay una partida en curso
        self.gameType = 1 # 1 = bots, 0 = 1v1, con 1 por defecto
        self.turno = 0
        self.winner = 2
        self.shared = 0 # Se refiere a si el resultado de la partida ha sido comunicado a ambos, si es así, se reinicia la partida completa 0 = no comunicado, 1 = 1 comunicado, 2 = ambos comunicados
        self.desconected = False
        self.surrender = False
        

    def iniciarPartida(self):
        if not self.partidaEnCurso:
            if(len(self.jugadoresConectados)<2 and self.gameType == 0):
                print("Como hay un solo jugador conectado, se ha asignado automáticamente el modo de juego contra bots")
                self.gameType = 1
            self.partidaEnCurso = True
            print("Partida iniciada")
        else:
            print("Ya hay una partida en curso")

    def finalizarPartida(self):
        if self.partidaEnCurso:
            # Lógica para finalizar una partida
            # Esto podría incluir el cálculo de resultados, limpieza de la partida, etc.
            self.winner = 0
            self.turno = 0
            self.partidaEnCurso = False
            self.shared = 0

            print("Partida finalizada")
        else:
            print("No hay una partida en curso")

    def __str__(self) -> str:
        
        return self
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


# Creamos instancia de un bot por si el usuario juega vs bots

bot = Bot()

bot.genShips()  #Genera barcos aleatorios para el bot
# Escucha para recibir datagramas entrantes
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode(encoding='utf-8', errors='strict')    # MENSAJE
    data = json.loads(message)
    
    address = bytesAddressPair[1][1]   #PUERTO
    clientIp_recv = bytesAddressPair[1][0]  #IP
    client_address = (clientIp_recv, address)
    
    print("DATA RECIBIDA OJITO ACAAAAA:   ")
    print(data)
    
    jugador_encontrado = False
    positionPlayer = 0
    
    for i in range(len(servidor.jugadoresConectados)):
        if(servidor.jugadoresConectados[i].ip == clientIp_recv and servidor.jugadoresConectados[i].port == address):
            positionPlayer = i
            jugador_encontrado = True
    
    
    if(servidor.partidaEnCurso and jugador_encontrado):   ## SOLO DEJA JUGAR A JUGADORES EN LA PARTIDA
        
        
        if(data["action"] == "a"):
            
            # CASO EN QUE SEA UN BOT
            if(servidor.gameType == 1):
                coords = data["position"]
                print("El usuario atacó acá: {}".format(coords))
                playerHit = 0
                
                #Ver si el usuario le dio a un barco del bot
                for i in range(len(bot.coordsShips)):
                    if(bot.coordsShips[i] == coords):
                        bot.lives = bot.lives-1
                        bot_index = i
                        playerHit = 1
                        
                        
                #Ver si el bot le dio a un barco del usuario
                botCoords = bot.attack()
                
                print("El bot atacó en la coordenada: ")
                print(botCoords)
                for i in range(len(servidor.jugadoresConectados[positionPlayer].coordsShips)):
                    if(servidor.jugadoresConectados[positionPlayer].coordsShips[i] == botCoords):
                        servidor.jugadoresConectados[positionPlayer].lives = servidor.jugadoresConectados[positionPlayer].lives -1
                
                
                print("Vidas del bot: ")
                print(bot.lives)
                print("Vidas del usuario: ")
                print(servidor.jugadoresConectados[positionPlayer].lives)
                print("Ha habido un ataqueeee")
                
                #TODO: Ver si ganó alguno
                
                if(bot.lives == 0):
                    print("Ha ganado el jugador")
                    aM = json.dumps(winMessage(botCoords))
                    returnedSignal(client_address, aM)
                    servidor.winner = positionPlayer
                    
                    servidor.finalizarPartida()
                    servidor.jugadoresConectados[positionPlayer].lives = 6
                    #reinicio del bot
                    bot.restart()
                    bot.genShips()

                     
                if(servidor.jugadoresConectados[positionPlayer].lives == 0):
                    print("Ha ganado el bot")
                    aM = json.dumps(loseMessage(botCoords))
                    returnedSignal(client_address, aM)
                    servidor.finalizarPartida()
                    servidor.jugadoresConectados[positionPlayer].lives = 6
                    
                    #Reinicio del bot
                    bot.restart()
                    bot.genShips()
                    
                    
                else:
                    #mensaje de retorno donde ninguno ha ganado aún
                    
                    aM = json.dumps(atackMessage(playerHit, botCoords))
                    returnedSignal(client_address, aM)
                       
   
                
            elif(servidor.gameType == 0):
                
                if(positionPlayer!=servidor.turno):
                    
                    messageR = json.dumps(turnMessage(0))
                    returnedSignal(client_address, messageR)
                else:


                    
                    print("------------------------ CONTROLLLL -----------------------------------")
                    
                    print( "position player actual {}".format(positionPlayer))
                    print( "VIDAS player actual {}".format(servidor.jugadoresConectados[positionPlayer].lives))
                    if(servidor.surrender == False and servidor.desconected == False):
                        print( "position player siguiente {}".format(abs(positionPlayer-1)))
                        print( "VIDAS player siguiente {}".format(servidor.jugadoresConectados[abs(positionPlayer-1)].lives))
                    else:
                        print("El otro jugador se desconectó")
                    print("Cantidad de jugadores actuales {}".format(len(servidor.jugadoresConectados)))
                    print("------------------------ CONTROLLLL -----------------------------------")
                    
                    playerHit = 0
                    #Atacar a los barcos del enemigo
                    if(servidor.surrender == False and servidor.desconected == False):
                    
                        for i in range(len(servidor.jugadoresConectados[abs(positionPlayer-1)].coordsShips)):
                            if(servidor.jugadoresConectados[abs(positionPlayer-1)].coordsShips[i] == data["position"]):
                                servidor.jugadoresConectados[abs(positionPlayer-1)].lives = servidor.jugadoresConectados[abs(positionPlayer-1)].lives -1                            
                                playerHit = 1
                        
                    
                    
                    #Ver si no tiene vidas por el ataque del jugador anterior
                    
                    if(servidor.jugadoresConectados[positionPlayer].lives < 1):
                        lose = json.dumps(loseMessage([0,0]))
                        returnedSignal(client_address, lose)
                        servidor.shared = servidor.shared +1 ##Se le comunicó a uno
                        
                    elif(servidor.surrender == True or servidor.desconected == True or servidor.jugadoresConectados[abs(positionPlayer-1)].lives < 1):
                        win = json.dumps(winMessage([0,0]))
                        returnedSignal(client_address, win)
                        servidor.shared = servidor.shared +1 ## Se le comunicó a otro
                                        

                    else:
                        aM = json.dumps(atackMessage(playerHit, [0,0]))
                        returnedSignal(client_address, aM)
                    
                        #Cambia el turno 
                    
                    servidor.turno = abs(servidor.turno -1)
                    

                    if(servidor.shared == 2):
                        
                        print("REINICIAR TODA LA PARTIDA")
                        servidor.jugadoresConectados[positionPlayer].lives = 6
                        servidor.jugadoresConectados[positionPlayer].coordsShips = []
                        if( servidor.desconected == False and servidor.surrender == False):
                            servidor.jugadoresConectados[abs(positionPlayer-1)].coordsShips = []
                            servidor.jugadoresConectados[abs(positionPlayer-1)].lives = 6
                        #todo DEL lado del cliente se tiene que volver a un status inicial, así no pueden atacar nuevamente, etc
                        servidor.finalizarPartida()
                        servidor.desconected = False
                        servidor.surrender = False
                    
                    
                    
                    
                    #Revisa si con el ataque anterior ganó o si antes de ganar se había quedado sin vidas

                    
                     

                
            
            
            print("Jugador {} está atacando".format(positionPlayer))
        
        if(data["action"] == "l"):
            aM = json.dumps(loseMessage([0,0]))
            returnedSignal(client_address, aM)
            servidor.turno = abs(servidor.turno -1)
            
            if(servidor.gameType == 1):
                #Reinicio del bot
                bot.restart()
                bot.genShips()
            else:
                servidor.jugadoresConectados[positionPlayer].lives = 0 #si es contra otro jugador, solo lo saca
                servidor.shared = 1
            
            bot.restart()
            bot.genShips()
            print("Se ha Rendido un usuario")

            
            
        if(data["action"] == "t"):
            if(positionPlayer!=servidor.turno):
                aM = json.dumps(turnMessage(0))
                returnedSignal(client_address, aM)
            else:
                aM = json.dumps(turnMessage(1))
                returnedSignal(client_address, aM)
                
        if(data["action"] == "d"):
            aM = json.dumps(disconnectMessage())
            returnedSignal(client_address, aM)
            servidor.nJugadores == servidor.nJugadores -1
            if(servidor.turno == positionPlayer):
                servidor.turno = 0
            
            if(servidor.gameType == 1):
                servidor.jugadoresConectados = [] #Si es 1 vs bot, vacía la lista
                servidor.finalizarPartida()
                #Reinicio del bot
                bot.restart()
                bot.genShips()
            else:
                servidor.jugadoresConectados.pop(positionPlayer) #si es contra otro jugador, solo lo saca
                servidor.desconected = True
                servidor.shared = 1
                if(len(servidor.jugadoresConectados)==0):
                    servidor.finalizarPartida()
                    
            
            bot.restart()
            bot.genShips()
            print("Se ha desconectado un usuario")
        if(data["action"] == "w"):
            if(servidor.jugadoresConectados[abs(positionPlayer-1)].lives < 1):
                win = json.dumps(winMessage([0,0]))
                returnedSignal(client_address, win)
            else:
                win = json.dumps(noWinMessage([0,0]))
                returnedSignal(client_address, win)

            

        
        
    
        
    
    
    
    
    
        
    if(jugador_encontrado):   #Con esto sabremos que el usuario está ya logueado
        
        ##################################################################
        # Acción build, que asigna los barcos y además inicia la partida #
        ##################################################################
        
        if(data["action"] == "b"):
            
            ## Si hay un solo jugador en el servidor, al iniciar la partida cambiará el modo de juego a vs bots
            if(len(servidor.jugadoresConectados) == 1):
                servidor.gameType = 1 
            
            #Si hay dos jugadores conectado, pero se quiere jugar vs bots, hechará al otro
            if(len(servidor.jugadoresConectados) == 2 and servidor.gameType == 1):
                servidor.jugadoresConectados.pop(abs(positionPlayer-1))
                servidor.nJugadores = 1
            print("NUMERO DE JUGADORES: ")
            print(len(servidor.jugadoresConectados))
            
            # Agregar patrullero (1x1)
            
            servidor.jugadoresConectados[positionPlayer].coordsShips.append(data["ships"]["p"][:2]) #Agregar patrullero [x,y]
            
            # Agregar barco (2x1)
            
            bXY = data["ships"]["b"][:2]  # [x,y]
            oB = data["ships"]["b"][-1]  # [orientación del barco]  0 = vertical, 1 = horizontal
            
            #Agregamos el nuevo barco
            servidor.jugadoresConectados[positionPlayer].coordsShips.append(bXY)
            
            #Debe revisar si no se van de los bordes, si se pasan entonces deben empezar a rellenarse desde la izquierda o arriba pq por defecto es hacia abajo u derecha
            
            if(oB == 1):
                if(bXY[0]+1 > 4):
                    bXY2 = [bXY[0]-1, bXY[1]] #se pasa del borde derecho    
                else:
                    bXY2 = [bXY[0]+1, bXY[1]] #No se pasa del borde derecho
                servidor.jugadoresConectados[positionPlayer].coordsShips.append(bXY2)
            elif(oB == 0):
                if(bXY[1]+1 > 4):
                    bXY2 = [bXY[0], bXY[1]-1] #se pasa del borde inferior    
                else:
                    bXY2 = [bXY[0], bXY[1]+1] #No se pasa del borde inferior
                servidor.jugadoresConectados[positionPlayer].coordsShips.append(bXY2)
            
            borderCondition = False
            #Agregar submarino (3x1)
            sXY = data["ships"]["s"][:2]  # [x,y]
            oS = data["ships"]["s"][-1]  # [orientación del barco]  0 = vertical, 1 = horizontal
            servidor.jugadoresConectados[positionPlayer].coordsShips.append(sXY)
            for i in range(2):
                if(oS==1):
                    if(sXY[0]+i+1>4):
                        if(not borderCondition):
                            sXY2 = [sXY[0]-1, sXY[1]] #Se pasa del borde
                            borderCondition = True
                        else:
                            sXY2 = [sXY[0]-i-1, sXY[1]] #Se pasa del borde
                            
                    else:
                        sXY2 = [sXY[0]+i+1, sXY[1]] #No se pasa del borde
                    servidor.jugadoresConectados[positionPlayer].coordsShips.append(sXY2)
                elif(oS == 0):
                    if(sXY[1]+i+1 > 4):
                        if(not borderCondition):
                            sXY2 = [sXY[0], sXY[1]-1] #se pasa del borde inferior    
                            borderCondition = True
                        else:
                            sXY2 = [sXY[0], sXY[1]-1-i] #se pasa del borde inferior    
                    else:
                        sXY2 = [sXY[0], sXY[1]+i+1] #No se pasa del borde inferior
                    servidor.jugadoresConectados[positionPlayer].coordsShips.append(sXY2)
            
            
            #Inicializa partida
            print(" PLAYER SHIPS")
            for i in range(len(servidor.jugadoresConectados[positionPlayer].coordsShips)):
                print(servidor.jugadoresConectados[positionPlayer].coordsShips[i])
            servidor.iniciarPartida()
            returnedSignal(client_address, buildMessageSuccess())
            
            
            #Devolver mensaje de inicio de partida correcto
            
            print("El usuario quiere iniciar una partida")
        
        
        ################################################################
        ### Lógica para elegir el tipo de partida, 1 = bots, 0 = 1v1 ###
        ################################################################
        
        if(data["action"] == "s"):
            print("Selección: {} como modo de juego".format(data["bot"]))
            returnedSignal(client_address, selectMessageSuccess())

            if(data["bot"] == 1):
                servidor.gameType = 1
                
                print("Partida contra bots")
            elif(data["bot"] == 0):
                
                servidor.gameType = 0    
                print("Partida 1 v 1 creada pero vacía")
            
            
    
    
        #####################################
        ### EL jugador no está "logueado" ###
        #####################################
    else:
        ##### Agrega nuevos jugadores a el servidor
        if(data["action"] == "c" and len(servidor.jugadoresConectados)<2 and servidor.partidaEnCurso == False):
        # Llama a la función returnedSignal() para enviar un mensaje al cliente
        # Construye mensajes para imprimir en la consola
            print("Se ha conectado un nuevo jugador ".format(address))
            servidor.jugadoresConectados.append(Jugador("Jugador {}".format(address), clientIp_recv, address,6))   ##AGREGA EL CLIENTE A LOS JUGADORES CONECTADOS
            servidor.nJugadores = servidor.nJugadores +1
            print(" Número de jugadores conectados = {}".format(len(servidor.jugadoresConectados)))
            
            ##
            returnedSignal(client_address, connectMessageSuccess())
            # returnedSignal(client_address, response_msg="CLIENTE: {}, de nombre: {}, Te has conectado de manera correcta".format(address, servidor.jugadoresConectados[0].nombre))
            

        else:
            print("Un usuario ha intentado conectarse pero el servidor está lleno")
            returnedSignal(client_address, connectFailMessage())

    

    
    
    
    
    
    
 