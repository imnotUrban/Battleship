def isOnList(list, item):

    for x in list:
        if(x == item):
            return True    
    return False


def indexOnList(list, item):
    for i in range(len(list)):
        if(list[i] == item): 
            return i
    
    return False



def drawBoard(board):
    
    for i in range(len(board)) :  
        for j in range(len(board[i])) :  
            print(" [{}] ".format(board[j][i]), end="")
        print("")
    

def createBoard():
    
    board = [[" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "]]
    
    return board


def fillBoard(board, attack, impact):   #arrBoats = [[1,1], [2,2], [3,3]]
    

    
    if(impact):
        board[attack[0]][attack[1]] = "X"
    else:
        board[attack[0]][attack[1]] = "-"
        
    
    
    return board