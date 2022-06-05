from ast import Break
from turtle import position
from piece import King, Bishop, Tower, Queen, Horse
import numpy as np


class Game():
# board bitmap 
# pieces lista de letras

    def __init__(self, board_size , snake_pos, pieces):
        self.__size = board_size;
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
        
        states = 1
        free_slots = 0
        for l in range (len(self.__board)):
            for c in range (len(self.__board_size)):
                if (self.__board == 0):
                    free_slots += 1

        states = 1 + pow(free_slots, len(self.__pieces) - 1)

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


    def getReward(self):
        if  len(self.__pieces) != 0 : 

            curr_num = self.__played[0].AttackNum(self.__board)

            for piece in self.__played:
                num_attacks = piece.AttackNum( self.__board)
                if ( curr_num != num_attacks):
                        return -10
            return 20 + ( 10 * num_attacks)

        return 0


    def move(self, action):
        #se a action for um numero é o indice de possible moves

        self.__state += ( self.__state * action ) 

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

        positions = []
        for i in range(len(self.__played)):
            pos_played = self.__played[i].getPos()
            if (pos_played[0] == pos[0] and pos_played[1]== pos[1]):
                return -20, self.__state
            positions.append(pos_played)

        piece_allocked.setAttack(self.__played)
        self.__played.append(piece_allocked)

        #check if it is the end 
        return self.getReward(), self.__state


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

