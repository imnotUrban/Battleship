class Partida:
    def __init__(self, id, pType, pstate):
        self.id = id   #ID UNICO
        self.players = [] # LISTA DE JUGADORES o 1 SI ES QUE ES CON BOTS
        self.pType = pType # ES EL TIPO, 1 = bots, 0 = 1 v 1
        self.pstate = pstate  # el estado será 0 = sin iniciar, 1 = un usuario ha confirmado su inicio (solo para no bots), 2 = dos usuarios han confirmado su inicio (solo para no bots), 3 = partida iniciada, 4 = partida finalizada
        self.winner = "" #Ganador de la partida
        self.shift = 0 #El primer jugador que sea introducido en la partida, jugará

    # def conectarAServidor(self, servidor):
    #     self.servidor = servidor
    #     servidor.jugadoresConectados.append(self)

    # def desconectar(self):
    #     if self.servidor:
    #         self.servidor.jugadoresConectados.remove(self)
    #         self.servidor = None

    # def jugarTurno(self):
    #     # Lógica para que el cliente juegue su turno
    #     pass    

    # def __init__(self, id, pType, pstate):
    #     self.id = id   #ID UNICO
    #     self.players = [] # LISTA DE JUGADORES o 1 SI ES QUE ES CON BOTS
    #     self.pType = pType # ES EL TIPO, 1 = bots, 0 = 1 v 1
    #     self.pstate = pstate  # el estado será 0 = sin iniciar, 1 = un usuario ha confirmado su inicio (solo para no bots), 2 = dos usuarios han confirmado su inicio (solo para no bots), 3 = partida iniciada, 4 = partida finalizada
    #     self.winner = "" #Ganador de la partida
    #     self.shift = 0 #El primer jugador que sea introducido en la partida, jugará
