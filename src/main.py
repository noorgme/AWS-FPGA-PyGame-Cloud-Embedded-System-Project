import pygame as pg
from enum import Enum
from sys import exit
import os
from pathlib import Path



#Set working directory
proj_folder = str(os.path.dirname((os.path.dirname(os.path.realpath(__file__)))))
os.chdir(proj_folder+"\include")


#define game states
class GameState(Enum):
    TITLESCREEN = 0
    LOGINSCREEN = 1
    #TO-DO: Add remaining game states

class GameStateManager:
    def __init__(self):
        self.current_state = None
    
    def change_state(self, new_state):
        self.current_state = new_state

    def run_state(self):
        if self.current_state == GameState.TITLESCREEN:
            titlescreen()
        elif self.current_state == GameState.LOGINSCREEN:
            loginscreen()

#Define Screen Functions


def titlescreen():

    titleMsg1 = font1.render("Press any key to continue", True," white")
    titleMsg1rect = titleMsg1.get_rect()
    titleMsg1rect.center = (screenWidth // 2, screenHeight //2 + 60)

    screen.fill("grey")
    #blit logo
    screen.blit(titleLogo, (screenWidth // 2 - titleLogo.get_width() // 2, screenHeight // 2 - titleLogo.get_height() // 2))

    #blit PressAnyKey
    screen.blit(titleMsg1, titleMsg1rect)

    pg.display.update()

def loginscreen():
    print ("loginscreen")
    # To-DO, code for loginscreen


pg.init()

#Initialize game state manager and set state = TitleScreen
game_state_manager = GameStateManager()
game_state_manager.change_state(GameState.TITLESCREEN)

#Setup display
screenWidth = 800
screenHeight = 500
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("FoodGame")

#Define Colours:
black = (0, 0, 0)
white = (255, 255, 255)

#Set Fonts
font1 = pg.font.Font(r"fonts\retro.ttf", 20)


#Setup clock
clock = pg.time.Clock()

#Load Media
titleLogo = pg.image.load(r"img\title.png").convert_alpha()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if game_state_manager.current_state == GameState.TITLESCREEN:
                game_state_manager.change_state(GameState.LOGINSCREEN)
                
    game_state_manager.run_state()
    # update display
    pg.display.update()

    # set FPS
    clock.tick(60)
