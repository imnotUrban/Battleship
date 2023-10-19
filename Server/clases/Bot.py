import random
class Bot:
    def __init__(self):
        self.nombre = "BOT"
        self.lives = 6
        self.coordsShips = []
        self.lastAttacks = []
   
   
    def restart(self):
        self.lives = 6
        self.coordsShips = []
        self.lastAttacks = []
   
   
    def attack(self):   #Donde atacó

        isNotTheAttackNew = True
        while(isNotTheAttackNew):
            isNotTheAttackNew = False
            x = random.randint(0,4)
            y = random.randint(0,4)
            for i in range(len(self.lastAttacks)):
                if(x == self.lastAttacks[i][0] and y == self.lastAttacks[i][1]):
                    isTheAttackNew = True
        self.lastAttacks.append([x,y])
        return [x,y]
            

    def genShips(self):
        
        coords = []
        
        ##Submarino
        dir = random.choice(['h', 'v'])
        if(dir == 'h'):
            x = random.randint(0,2)
            y = random.randint(0,2)
            for i in range(3):
                coords.append([x+i,y])
        elif(dir == 'v'):
            x = random.randint(0,2)
            y = random.randint(0,2)
            for i in range(3):
                coords.append([x,y+i])
                
        
        #barco 
        notUni = True   #las coords no son unicas
        dir = random.choice(['h', 'v'])
        while(notUni):   
            notUni = False
            if(dir == 'h'): 
                x = random.randint(0,3)
                y = random.randint(0,3)
                for i in range(3):
                    if([x,y] == coords[i]):
                        notUni = True
                    if([x+1,y] == coords[i]):
                        notUni = True
                if(notUni == False):
                    coords.append([x,y])
                    coords.append([x+1,y])
                    
            if(dir == 'v'): 
                x = random.randint(0,3)
                y = random.randint(0,3)
                for i in range(3):
                    if([x,y] == coords[i]):
                        notUni = True
                    if([x,y+1] == coords[i]):
                        notUni = True
                if(notUni == False):
                    coords.append([x,y])
                    coords.append([x,y+1])

        #Patrullero
        
        notUnique = True
        while(notUnique):
            notUnique = False
            x = random.randint(0,4)
            y = random.randint(0,4)
            for i in range(len(coords)):
                if([x,y] == coords[i]):
                    notUnique = True
        coords.append([x,y])
                    
        
        
        self.coordsShips = coords
        
        return coords

bot = Bot()

bot.genShips()

