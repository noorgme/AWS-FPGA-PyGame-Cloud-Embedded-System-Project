import pygame as pg
from enum import Enum
from sys import exit
import os


#Set working directory
proj_folder = str(os.path.dirname((os.path.dirname(os.path.realpath(__file__)))))
os.chdir(proj_folder+"\include")


#define game states
class GameState(Enum):
 
    CHARACTERSELECT = 0
    
    #TO-DO: Implement remaining game states

class GameStateManager:
    def __init__(self):
        self.current_state = None
    
    def change_state(self, new_state):
        self.current_state = new_state

    def run_state(self):
        # if self.current_state == GameState.TITLESCREEN:
        #     titlescreen()
        # elif self.current_state == GameState.LOGINSCREEN:
        #     loginscreen()
        # elif self.current_state == GameState.PLAYERCONNECT:
        #     playerconnect()
        if self.current_state == GameState.CHARACTERSELECT:
            characterselect()
        # elif self.current_state == GameState.MAINGAME:
        #     maingame()

#Define player class
class Player:
    def __init__(self, name, character, hasBomb, isAlive, playernum):
        self.name = name
        self.character = character
        self.hasBomb = hasBomb
        self.isAlive = isAlive
        self.img = pg.image.load("img/"+character+".png").convert_alpha()
        if playernum == 1:
            playerpos = (screenWidth//2, screenHeight//2+200)
        if playernum == 2:
            playerpos = (screenWidth//2 - 200, screenHeight//2-100)
        if playernum == 3:
            playerpos = (screenWidth//2+200, screenHeight//2-100)
        self.img = pg.transform.scale(self.img, (150, 150))
        self.player_rect = self.img.get_rect(center = playerpos)
    
    def throwBomb(self, direction):
        print ("Bomb thrown to " + str(direction))

#Define Screen Functions
def characterselect():
    
    
     # Define square dimensions and spacing
    square_size = 220
    square_spacing = 70
   
     #load character images
    characters = ["sarim", "bouganis", "naylor"]
    player1 = Player("noor", characters[0], hasBomb = True, isAlive = True, playernum = 1)
    player2 = Player("shaheer", characters[1], hasBomb = False, isAlive = True, playernum =  2)
    player3 = Player("jim", characters[2], hasBomb = False, isAlive = True, playernum = 3)
   

    bomb_img = pg.image.load("img/bomb.png").convert_alpha()
    bomb_img = pg.transform.scale(bomb_img, (70, 70))
    
   
    characters_1 = pg.image.load("img/sarim.png").convert_alpha()
    characters_2 = pg.image.load("img/bouganis.png").convert_alpha()
    characters_3 = pg.image.load("img/naylor.png").convert_alpha()
    player1 = pg.image.load("img/sarim.png").convert_alpha()
    player2 = pg.image.load("img/sarim.png").convert_alpha()
    player3 = pg.image.load("img/sarim.png").convert_alpha()
    players = [player1, player2, player3]

    characters_1 = pg.transform.scale(characters_1, (300, 150))
    characters_1_trans = characters_1.copy()
    characters_1_trans.set_alpha(120)#Pass 0 for invisible and 255 for fully opaque.
    characters_1rect = characters_1.get_rect()

    characters_2 = pg.transform.scale(characters_2, (300, 150))
    characters_2_trans = characters_2.copy()
    characters_2_trans.set_alpha(120)
    characters_2rect = characters_3.get_rect()

    characters_3 = pg.transform.scale(characters_3, (300, 150))
    characters_3_trans = characters_3.copy()
    characters_3_trans.set_alpha(120)
    characters_3rect = characters_3.get_rect()
    
    # for player in players:
    #     player = pg.transform.scale(player, (300, 150))
    play=["jim","noor", "shaheer"]  
    for plays in play:
        waiting_msg1 = font1.render("Waiting for player to select..."+str(plays), True, black)
    waiting_msg2 = font1.render("No Character selected yet", True, black)
    waiting_msg2rect = waiting_msg2.get_rect()
    waiting_msg2rect.center = ((screenWidth // 2) + 30, screenHeight //2 + 60)

    success_msg = font1.render("Character successfully selected", True, black)
    success_msgrect = success_msg.get_rect()
    success_msgrect.center = ((screenWidth // 2) + 40, screenHeight //2 + 60)

    unsuccess_msg = font1.render("Character selected, please select another one", True, black)
    unsuccess_msgrect = unsuccess_msg.get_rect()
    unsuccess_msgrect.center = ((screenWidth // 2) + 40, screenHeight //2 + 60)

        
    squares = [
        [(screenWidth / 2) - 1.6*(square_size + square_spacing), screenHeight / 3 - 140],
        [(screenWidth / 2) - 1.2*(square_spacing), screenHeight / 3 - 140],
        [(screenWidth / 2) + (square_spacing + square_size), screenHeight / 3 - 140],

        [(screenWidth / 2) - 1.6*(square_size + square_spacing), screenHeight / 3 + 130],
        [(screenWidth / 2) - 1.2*(square_spacing), screenHeight / 3 + 130],
        [(screenWidth / 2) + (square_spacing + square_size), screenHeight / 3 + 130]

    ]
    niosCoords = [(squares[0][0] +125, squares[0][1]+110),
                  (squares[1][0] +125, squares[1][1]+110),
                  (squares[2][0] +125, squares[2][1]+110),
                  (squares[3][0] +125, squares[3][1]+110),
                  (squares[4][0] +125, squares[4][1]+110),
                  (squares[5][0] +125, squares[5][1]+110)
                  ]
    numPlayers = 3
    pg.display.flip()
    characters_rect=[characters_1rect,characters_2rect, characters_3rect]
    characters_rects=[]
    playersss=[]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONUP:
                for characters_r in characters_rect:
                    #for player in players:
                        if (characters_r.collidepoint(pg.mouse.get_pos())):
                     #       playersss.append(player)
                            characters_rects.append(characters_r)
                            for c in characters_rects:
                               if(characters_r != c):
                                  #player = Player(player, characters[0], hasBomb = True, isAlive = True, playernum = 1)
                                  print("successfully selected")
                                  #screen.blit(success_msg, (screenWidth / 2) - 1.2*(square_spacing), screenHeight / 3 + 130)
                                  screen.blit(success_msg,success_msgrect)
                               else :
                                  #screen.blit(unsuccess_msg, (screenWidth / 2) - 1.2*(square_spacing), screenHeight / 3 + 130)
                                  screen.blit(unsuccess_msg,unsuccess_msgrect)
                                  print("unsuccess")
                        else:
                            screen.blit(waiting_msg2,waiting_msg2rect)
                            print("else")
                
            screen.fill(light_grey)
           #draw squares
        #screen.blit(waiting_msg2,waiting_msg2rect)
        #screen.blit(waiting_msg1, (screenWidth / 2 - waiting_msg1.get_width() / 2, screenHeight - 100))
        #screen.blit(waiting_msg1, (squares[3][0] - 60, 50))
        for square in squares:
            pg.draw.rect(screen, blue, (square[0], square[1], square_size, square_size), border_radius=10)
        
        #for i in range(0,numPlayers):
            #de10rect.center = niosCoords[i]
        characters_1rect.center = niosCoords[0]
        characters_2rect.center = niosCoords[4]
        characters_3rect.center = niosCoords[2]
        screen.blit(characters_1, characters_1rect)
        screen.blit(characters_2, characters_2rect)
        screen.blit(characters_3, characters_3rect)
        
        # for i in range(0, 6-numPlayers):
        #     de10rect.center = niosCoords[5-i]
        #     screen.blit(de10_trans, de10rect)
        pg.display.flip()

pg.init()

#Initialize game state manager and set state = TitleScreen
game_state_manager = GameStateManager()
game_state_manager.change_state(GameState.CHARACTERSELECT)

#Setup display
screenWidth = 1280
screenHeight = 720
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("FoodGame")

#Define Colours:
black = (0, 0, 0)
white = (255, 255, 255)
light_grey = (200, 200, 200)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


#Set Fonts
font1 = pg.font.Font(r"fonts\retro.ttf", 20)


#Setup clock
clock = pg.time.Clock()

#Load Media
titleLogo = pg.image.load(r"img\title.png").convert_alpha()

def main():
    game_state_manager.run_state()

main()