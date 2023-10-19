#MENSAJE PARA SOLICITAR CONEXIÓN
def messageConnection():  
    
    return '{"action": "c","bot": 0, "ships": {"p": [1,1,0], "b":[1,2,0], "s": [1,1,0]},"position": [1,1]}'

#MENSAJE PARA ELEGIR EL MODO DE JUEGO
def messageBots(type):
    if(type == 1 or type == "1"):
        return '{"action": "s","bot": 1, "ships": {"p": [1,1,0], "b":[1,2,0], "s": [1,1,0]},"position": [1,1]}'
    if(type == 0 or type == "0"):
        return '{"action": "s","bot": 0, "ships": {"p": [1,1,0], "b":[1,2,0], "s": [1,1,0]},"position": [1,1]}'
    
#MENSAJE PARA EMPEZAR LA PARTIDA Y AL MISMO TIEMPO ENVIAR LOS BARCOS
def messageBuild(pArray, bArray, sArray):
    
    
    msg = {
    "action": "b", # build
    "bot": 0,
    "ships": {
                "p": pArray, # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
                "b": bArray,
                "s": sArray
            },
    "position": []
    }
    

    return msg

def messageAtack(arr):
    
    
    msg = {
    "action": "a", # build
    "bot": 0,
    "ships": {
                "p": [], # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
                "b": [],
                "s": []
            },
    "position": arr
    }
    

    return msg

def messageDisconnect():   #TODO Debe enviar para que lo borren de la lista de usuarios, dsp solito se debe desconectar
    
    msg = {
    "action": "d", # disconnect
    "bot": 0,
    "ships": {
                "p": [], # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
                "b": [],
                "s": []
            },
    "position": []
    }
    

    return msg


def messageSurrender():
    
    msg = {
    "action": "l", # l = surrender
    "bot": 0,
    "ships": {
                "p": [], # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
                "b": [],
                "s": []
            },
    "position": []
    }
    

    return msg

def messageTurn():
    
    msg = {
    "action": "t", # t = consulta turno
    "bot": 0,
    "ships": {
                "p": [], # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
                "b": [],
                "s": []
            },
    "position": []
    }
    

    return msg