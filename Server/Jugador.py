class Jugador:
    def __init__(self, nombre, ip, port, lives):
        self.nombre = nombre
        self.ip = ip
        self.port = port
        self.lives = lives
        self.coordsShips = []

    def realizarAccion(self, coordenada):
        # Lógica para realizar una acción en una coordenada
        pass