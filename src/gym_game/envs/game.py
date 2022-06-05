from gym_game.envs.piece import King, Bishop, Tower, Queen, Horse
import numpy as np


class Game():
# board bitmap 
# pieces lista de letras

    def __init__(self, board_size , snake_pos, pieces):
        self.__size = board_size
        self.__board = np.full([board_size, board_size], 0)
        self.__move = 0 # indice of piece being played
        self.__state = 0 # state of game
        self.__played = [] # list pieces chosen
        self.__possible_moves = [] # free slots
        self.__snake = snake_pos

        for pos in range(len(snake_pos)):
            self.__board[ snake_pos[pos][1]][snake_pos[pos][0]] = 1

        for l in range (board_size):
            for c in range (board_size):
                if ( self.__board[l][c] == 0):
                    self.__possible_moves.append([l,c])
        
        
        self.__pieces = pieces 

    def calculatePossibleStates(self):
        states = 0
        for i in range(1,len(self.__pieces) ):
            states += len(self.__possible_moves) ^ i
        
        if (states == 0):
            states = 1

        return states
    
    def getPossibleMoves(self):
        return self.__possible_moves

    def getSize(self):
        return self.__size

    def getState(self):
        return self.__state

    def getPieces(self):
        return self.__pieces

    def getSnake(self):
        return self.__snake

    def getPositionPlayed(self):
        return self.__played

    


    def getReward(self):
        
        if (self.done()):

            curr_num = self.__played[0].AttackNum(self.__board)

            for piece in self.__played:
                num_attacks = piece.AttackNum( self.__board)
                if ( curr_num != num_attacks):
                    return -30
            return 20 + ( 10 * num_attacks)
        
        elif len(self.__played) != 1 : 
            curr_num = self.__played[ self.__move - 2].AttackNum(self.__board)
            num_attacks = self.__played[ self.__move - 1 ].AttackNum(self.__board)
            
            if (curr_num != num_attacks):
                return -5
            else:
                return 2 + ( 10 * num_attacks)

        return 0


    def move(self, action):
        #se a action for um numero é o indice de possible moves

        pos = self.__possible_moves[action]

        piece = self.__pieces[self.__move]

        if (piece == 'H'):
            piece_allocked = Horse(pos[0], pos[1], len(self.__board)) 
        elif (piece == 'Q'):
            piece_allocked = Queen(pos[0], pos[1], len(self.__board)) 
        elif (piece == 'B'):
            piece_allocked = Bishop(pos[0], pos[1], len(self.__board)) 
        elif (piece == 'K'):
            piece_allocked = King(pos[0], pos[1], len(self.__board))
        elif (piece == 'T'):
            piece_allocked = Tower(pos[0], pos[1], len(self.__board))

        positions = []
        for piece in self.__played:
            ocupied_pos = piece.getOcupiedPos()
            ocupied_pos.append(pos)
            piece.setAttack(ocupied_pos)
            ocupied_pos = []
            pos_played = piece.getPos()
            positions.append(pos_played)

        piece_allocked.setAttack(positions)
        self.__played.append(piece_allocked) 

        for pos_played in positions:
            if (pos_played[0] == pos[0] and pos_played[1]== pos[1]):
                return -40, self.__state, True

        
        if (not self.done()):
            self.__state += ( action + 1 ) ^ self.__move

        self.__move +=1


        #check if it is the end 
        return self.getReward(), self.__state, self.done()


    def display(self):
        board_size = len(self.__board)

        found = False
        for l in range (board_size):
            for c in range (board_size):
                if (self.__board[l][c] == 1):
                    print(" 1 ", end ="")
                else:
                    for piece in self.__played:
                        if piece.getPos()[0] == c and piece.getPos()[1] == l:
                            found = True
                            print(" H ", end ="")
                            break
                    if(not found):
                        print(" E ", end ="")
                    found = False
            print("\n")

    def done(self):
        if (len(self.__played) == len(self.__pieces)):
            return True
        return False
                    
                    

"""  

pieces = ['H', 'H']
game = Game( 3, [[0,2],[1,2], [1, 1], [2,1], [2,0]], pieces)

reward = 0
i = 0
while(reward == 0):
    game.display()


    for action in game.getPossibleMoves():
        print(action)

    col = input("Enter your action: ")
    
    reward, state = game.move(int(col))
    i+=1
    print("reward ", reward)

game.display()

 """