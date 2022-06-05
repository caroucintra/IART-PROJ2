from operator import truediv
import numpy as np


class Piece:
    _col = 0
    _line = 0
    _board_size = 0
    _bitmap = []
    
    def __init__(self, col, line, board_size):
        """ Builds the piece 

        Args:
            col (int): piece's column in the board
            line (int): piece's line in the board
            board_size (int): size of the board, the number of collumns is equal to the number of lines
        """
        self._col = col
        self._line = line
        self._board_size = board_size
    
    def setAttack(self, positions):
        """ Builds the bitmap corresponding to the piece's attacks

        Args:
            positions (vector): vector with the positions of all the pieces in the board
        """
        self._bitmap = np.array([[0]*(self._board_size)]*(self._board_size))

    def AttackNum(self, snake):
        """Evaluates how many times the piece attacks a snake

        Args:
            snake (Snake): snake to evaluate

        Returns:
            int: number of times the piece attacks the snake
        """
        num = 0
        
        for l in range (self._board_size):
            for c in range (self._board_size):
                if (snake[l][c] and self._bitmap[l][c]):
                    num += 1
        return num

    def getPos(self):
        return [self._line,self._col]
    
    def getAttack(self):
        return self._bitmap
   

    def diagonalAttack(self, positions):
        """Records in the piece's bitmap the slots the piece atacks with the the diagonal attack

        Args:
            positions (vector): the positions of the pieces in the board
        """
        xnyn = True
        xnyp = True
        xpyn = True
        xpyp = True
        i = 1
        while ( xnyn or xnyp or xpyn or xpyp) :
            if ( self._line - i >= 0 and self._col - i >= 0 and xnyn ):
                for pos in positions:
                    if (pos[0] == self._col - i and pos[1] == self._line - i):
                        xnyn = False
                        break

                self._bitmap[self._line - i, self._col - i] = 1
            else : xnyn = False

            if ( self._line + i < self._board_size and self._col - i >= 0 and xnyp ):
                for pos in positions:
                    if (pos[0] == self._col - i and pos[1] == self._line + i):
                        xnyp = False
                        break

                self._bitmap[self._line + i, self._col - i] = 1
            else : xnyp = False

            if ( self._line - i >= 0 and self._col + i < self._board_size and xpyn ):
                for pos in positions:
                    if (pos[0] == self._col + i and pos[1] == self._line - i):
                        xpyn = False
                        break

                self._bitmap[self._line - i, self._col + i] = 1
            else : xpyn = False 

            if ( self._line + i < self._board_size and self._col + i < self._board_size and xpyp ):
                for pos in positions:
                    if (pos[0] == self._col + i and pos[1] == self._line + i):
                        xpyp = False
                        break

                self._bitmap[self._line + i, self._col + i] = 1
            else : xpyp = False 

            i += 1

    def orthogonalAttack(self, positions):
        """Records in the piece's bitmap the slots the piece atacks with the the orthogonal attack

        Args:
            positions (vector): the positions of the pieces in the board
        """
        up = True 
        down = True
        left = True
        right = True
        i = 1

        while (up or down or left or right):
            if ( self._line - i >= 0 and up):
                for pos in positions:
                    if (pos[0] == self._col and pos[1] == self._line - i):
                        up = False
                        break
                self._bitmap[self._line - i][self._col] = 1
            else: 
                up = False
            if ( self._line + i < self._board_size and down):
                for pos in positions:
                    if (pos[0] == self._col and pos[1] == self._line + i):
                        down = False
                        break
                self._bitmap[self._line + i][self._col] = 1
            else: 
                down = False
            if ( self._col + i < self._board_size and right):
                for pos in positions:
                    if (pos[0] == self._col + i and pos[1] == self._line):
                        right = False
                        break
                self._bitmap[self._line][self._col + i] = 1
            else: 
                right = False
            if ( self._col - i >= 0 and left):
                for pos in positions:
                    if (pos[0] == self._col - i and pos[1] == self._line):
                        left = False
                        break
                self._bitmap[self._line][self._col - i] = 1
            else: 
                left = False

            i += 1


class Tower(Piece):
    def __init__(self, col, line, board_size):
        super().__init__(col, line, board_size)
    
    def setAttack(self, positions):
        super().setAttack( positions)
        super().orthogonalAttack(positions)

class Bishop(Piece):
    def __init__(self, col, line, board_size):
        super().__init__(col, line, board_size)
    
    def setAttack(self, positions):
        super().setAttack(positions)
        super().diagonalAttack(positions)   

class Queen(Piece):
    def __init__(self, col, line, board_size):
        super().__init__(col, line, board_size)
    
    def setAttack(self, positions):
        super().setAttack( positions)
        super().diagonalAttack(positions)
        super().orthogonalAttack(positions)

class King(Piece):
    def __init__(self, col, line, board_size):
        super().__init__(col, line, board_size)

    def setAttack(self, positions):
        """Records in the piece's bitmap the slots the piece atacks with the the King attack

        Args:
            positions (vector): the positions of the pieces in the board
        """
        super().setAttack( positions)

        up = False
        down = False
        left = False
        right = False

        if ( self._line + 1 < self._board_size):
            self._bitmap[self._line + 1 ][self._col] = 1
            down = True 
        if ( self._line - 1 >= 0):
            self._bitmap[self._line - 1 ][self._col] = 1
            up = True 
        if ( self._col - 1 >= 0):
            self._bitmap[self._line][self._col - 1] = 1
            left = True
        if ( self._col + 1 < self._board_size):
            self._bitmap[self._line][self._col + 1] = 1
            right = True

        if ( up):
            if (right):
                self._bitmap[self._line - 1][self._col + 1] = 1
            if ( left):
                self._bitmap[self._line - 1][self._col - 1] = 1
        if ( down):
            if (right):
                self._bitmap[self._line + 1][self._col + 1] = 1
            if ( left):
                self._bitmap[self._line + 1][self._col - 1] = 1


class Horse(Piece):
    def __init__(self, col, line, board_size):
        super().__init__(col, line, board_size)
    
    def setAttack(self, positions):
        """Records in the piece's bitmap the slots the piece atacks with the the horse attack

        Args:
            positions (vector): the positions of the pieces in the board
        """
        super().setAttack(positions)

        l = self._line
        c = self._col
        if (l > 0):
            l -= 1
            if (l >= 0):
                if (c >= 2):
                    self._bitmap[l][c-2] = 1
                if (c <= self._board_size-3):
                    self._bitmap[l][c+2] = 1

            if (l > 0):
                l -= 1
                if (c >= 1):
                    self._bitmap[l][c-1] = 1
                if (c <= self._board_size-2):
                    self._bitmap[l][c+1] = 1

        l = self._line
        if (l < self._board_size -1):
            l += 1
            if (l <= self._board_size -1):
                if (c >= 2):
                    self._bitmap[l][c-2] = 1
                if (c <= self._board_size-3):
                    self._bitmap[l][c+2] = 1
            if (l < self._board_size -1):
                l += 1
                if (c >= 1):
                    self._bitmap[l][c-1] = 1
                if (c <= self._board_size-2):
                    self._bitmap[l][c+1] = 1

        l = self._line
        if (c > 0):
            c -= 1
            if (c >= 0):
                if (l >= 2):
                    self._bitmap[l-2][c] = 1
                if (l <= self._board_size -3):
                    self._bitmap[l+2][c] = 1
            if (c > 0):
                c -= 1
                if (l >= 1):
                    self._bitmap[l-1][c] = 1
                if (l <= self._board_size -2):
                    self._bitmap[l+1][c] = 1

        c = self._col
        if (c < self._board_size-1):
            c += 1
            if (c <= self._board_size-1):
                if (l >= 2):
                    self._bitmap[l-2][c] = 1
                if (l <= self._board_size -3):
                    self._bitmap[l+2][c] = 1
            if (c < self._board_size-1):
                c += 1
                if (l >= 1):
                    self._bitmap[l-1][c] = 1
                if (l <= self._board_size -2):
                    self._bitmap[l+1][c] = 1
