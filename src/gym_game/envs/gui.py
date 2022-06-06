from re import A
from unittest import result
from gym_game.envs import game
from gym_game.envs.piece import Bishop, Tower, Queen, Horse, King
from gym_game.envs.game import Game
import pygame
import pygame.freetype
import time

class GUI:
    BG = (0,0,0)
    DIV = (255,255,255)
    SNAKE = (28, 29, 83)
    SCREENWIDTH = 600
    SCREENHEIGHT = 600

    def __init__(self, board_size , snake_pos, pieces):
        
        self.game = Game(board_size, snake_pos, pieces)

    def getGame(self):
        return self.game

    def action(self, action):
        return self.game.move(action)

    def state(self):
        return self.game.getState()

    def reward(self):
        return self.game.getReward()

    def done(self):
        return self.game.done()

    def view(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self.SCREENWIDTH,self.SCREENHEIGHT))
        self.drawBoard(self.game.getSize(), self.game.getPositionPlayed(), self.game.getSnake())

    def drawBoard(self, size, pieces, snake):
        result = True
        while(result):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        result = False
            self._screen.fill(self.BG)
            self.size = size
            if size == 6:
                self.draw6x6()
            elif size == 5:
                self.draw5x5()
            elif size == 4:
                self.draw4x4()
            else:
                self.draw3x3()

            self.setPieces(pieces)
            self.setSnake(snake)
            pygame.display.update()



    def draw6x6(self):
        """Function that draws the lines for a 6x6 board
        """
        pygame.draw.line(self._screen, self.DIV, [0,100], [self.SCREENWIDTH,100], 3)
        pygame.draw.line(self._screen, self.DIV, [0,200], [self.SCREENWIDTH,200], 3)
        pygame.draw.line(self._screen, self.DIV, [0,300], [self.SCREENWIDTH,300], 3)
        pygame.draw.line(self._screen, self.DIV, [0,400], [self.SCREENWIDTH,400], 3)
        pygame.draw.line(self._screen, self.DIV, [0,500], [self.SCREENWIDTH,500], 3)

        pygame.draw.line(self._screen, self.DIV, [100,0], [100,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [200,0], [200,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [300,0], [300,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [400,0], [400,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [500,0], [500,self.SCREENHEIGHT], 3)

    def draw5x5(self):
        """Function that draws the lines for a 5x5 board
        """
        pygame.draw.line(self._screen, self.DIV, [0,120], [self.SCREENWIDTH,120], 3)
        pygame.draw.line(self._screen, self.DIV, [0,240], [self.SCREENWIDTH,240], 3)
        pygame.draw.line(self._screen, self.DIV, [0,360], [self.SCREENWIDTH,360], 3)
        pygame.draw.line(self._screen, self.DIV, [0,480], [self.SCREENWIDTH,480], 3)

        pygame.draw.line(self._screen, self.DIV, [120,0], [120,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [240,0], [240,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [360,0], [360,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [480,0], [480,self.SCREENHEIGHT], 3)

    def draw4x4(self):
        """Function that draws the lines for a 5x5 board
        """
        pygame.draw.line(self._screen, self.DIV, [0,150], [self.SCREENWIDTH,150], 3)
        pygame.draw.line(self._screen, self.DIV, [0,300], [self.SCREENWIDTH,300], 3)
        pygame.draw.line(self._screen, self.DIV, [0,450], [self.SCREENWIDTH,450], 3)

        pygame.draw.line(self._screen, self.DIV, [150,0], [150,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [300,0], [300,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [450,0], [450,self.SCREENHEIGHT], 3)
    
    def draw3x3(self):
        """Function that draws the lines for a 5x5 board
        """
        pygame.draw.line(self._screen, self.DIV, [0,200], [self.SCREENWIDTH,200], 3)
        pygame.draw.line(self._screen, self.DIV, [0,400], [self.SCREENWIDTH,400], 3)

        pygame.draw.line(self._screen, self.DIV, [200,0], [200,self.SCREENHEIGHT], 3)
        pygame.draw.line(self._screen, self.DIV, [400,0], [400,self.SCREENHEIGHT], 3)


    def setPieces(self, vec):
        """Function that creates the sprites for each piece and draws it in the screen

        Args:
            vec (vector): vector with the Piece objects
        """
        size = self.game.getSize()
        sprites = pygame.sprite.Group()
        if size == 6:
            space = 100
        elif size == 5:
            space = 120
        elif size == 4:
            space = 150
        else:
            space = 200

        for v in vec:
            if isinstance(v,Tower):
                sprites.add(Tower_sprite(space, v))
            elif isinstance(v,Bishop):
                sprites.add(Bishop_sprite(space, v))
            elif isinstance(v,Queen):
                sprites.add(Queen_sprite(space, v))
            elif isinstance(v,King):
                sprites.add(King_sprite(space, v))
            else:
                sprites.add(Horse_sprite(space, v))
        sprites.draw(self._screen)

    def setSnake(self, snake):
        """Function that creates the rectangles that represent the snake in the board and draws them

        Args:
            snake (vector ints): snake positions
        """
        size = self.game.getSize()
        if size == 6:
            space = 100
        elif size == 5:
            space = 120
        elif size == 4:
            space = 150
        else:
            space = 200

        for bit in snake:
            pygame.draw.rect(self._screen, self.SNAKE, [space*bit[0],space*bit[1],space,space])


class Piece_sprite(pygame.sprite.Sprite):
    """Class that represents the chess pieces as sprites in the screen. 
    Each piece is loaded with an image representing the chess piece (King, Queen, Bishop, Tower, Horse)

    Args:
        pygame (Sprite): Superclass
    """
    _width = 0
    _height = 0
    def __init__(self, size, obj):
        super().__init__()
        self._line = obj._line
        self._col = obj._col

class Tower_sprite(Piece_sprite):
    def __init__(self, size, obj):
        super().__init__(size, obj)
        self.image = pygame.Surface([size, size])
        
        image1_not_scaled = pygame.image.load("resources/tower.png").convert_alpha()
        
        self.image = pygame.transform.scale(image1_not_scaled, [size, size])
 
        self.rect = self.image.get_rect()

        self.rect.x = self._col*size
        self.rect.y = self._line*size

class Queen_sprite(Piece_sprite):
    def __init__(self, size, obj):
        super().__init__(size, obj)
        self.image = pygame.Surface([size, size])
        
        image1_not_scaled = pygame.image.load("resources/queen.png").convert_alpha()
        
        self.image = pygame.transform.scale(image1_not_scaled, [size, size])
 
        self.rect = self.image.get_rect()

        self.rect.x = self._col*size
        self.rect.y = self._line*size

class Horse_sprite(Piece_sprite):
    def __init__(self, size, obj):
        super().__init__(size, obj)
        self.image = pygame.Surface([size, size])
        
        image1_not_scaled = pygame.image.load("resources/horse.png").convert_alpha()
        
        self.image = pygame.transform.scale(image1_not_scaled, [size, size])
 
        self.rect = self.image.get_rect()

        self.rect.x = self._col*size
        self.rect.y = self._line*size

class Bishop_sprite(Piece_sprite):
    def __init__(self, size, obj):
        super().__init__(size, obj)
        self.image = pygame.Surface([size, size])
        
        image1_not_scaled = pygame.image.load("resources/bishop.png").convert_alpha()
        
        self.image = pygame.transform.scale(image1_not_scaled, [size, size])
 
        self.rect = self.image.get_rect()

        self.rect.x = self._col*size
        self.rect.y = self._line*size

class King_sprite(Piece_sprite):
    def __init__(self, size, obj):
        super().__init__(size, obj)
        self.image = pygame.Surface([size, size])
        
        image1_not_scaled = pygame.image.load("resources/king.png").convert_alpha()
        
        self.image = pygame.transform.scale(image1_not_scaled, [size, size])
 
        self.rect = self.image.get_rect()

        self.rect.x = self._col*size
        self.rect.y = self._line*size

    def printPieceList(self):
        print(self.game.getPositionPlayed())
        
