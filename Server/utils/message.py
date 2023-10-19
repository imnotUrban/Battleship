
#Función que define el mensaje cuando ha habido una conexión correcta
def connectMessageSuccess():
    
    msg = '{"action": "c","status": 1,"position": [1,2]}'
    
    return msg



def connectFailMessage():
    msg = '{"action": "c","status": 0,"position": [1,2]}'
    
    return msg

#Función que define el mensaje cuando ha seleccionado de manera correcta el modo de juego
def selectMessageSuccess():
    
    msg = '{"action": "s","status": 1,"position": [1,2]}'
    
    return msg


def buildMessageSuccess():
    
    msg = '{"action": "b","status": 1,"position": [1,2]}'
    
    return msg

def atackMessage(hitUser, coords_bot):
    
    msg = {
    "action": "a", 
    "status": hitUser,
    "position": [coords_bot]
    }
    return msg
    

def winMessage(hitUser):

    msg = {
    "action": "w", 
    "status": 1,
    "position": [hitUser]
    }
    
    return msg
def noWinMessage(hitUser):

    msg = {
    "action": "w", 
    "status": 0,
    "position": [hitUser]
    }
    
    return msg

def loseMessage(hitUser):

    msg = {
    "action": "l", 
    "status": 1,
    "position": [hitUser]
    }
    
    return msg

def turnMessage(turn):  #turn puede ser 1 si era su turno, 0 si no

    msg = {
    "action": "t", 
    "status": turn,
    "position": []
    }
    
    return msg

def disconnectMessage():  #turn puede ser 1 si era su turno, 0 si no

    msg = {
    "action": "d", 
    "status": 1,
    "position": []
    }
    
    return msg