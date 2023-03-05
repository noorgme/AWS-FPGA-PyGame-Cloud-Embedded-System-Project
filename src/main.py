import pygame as pg
from enum import Enum
from sys import exit
import os


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

    
    titleMsg1 = font1.render("Press any key to continue", True,white)
    titleMsg1rect = titleMsg1.get_rect()
    titleMsg1rect.center = (screenWidth // 2, screenHeight //2 + 60)

    while True:
        clock.tick(60)
        framerate = font1.render(str(pg.time.get_ticks()), True, black)
        framerect = framerate.get_rect()
        framerect.bottomright = (screenWidth-10, screenHeight-20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if game_state_manager.current_state == GameState.TITLESCREEN:
                    game_state_manager.change_state(GameState.LOGINSCREEN)
                    game_state_manager.run_state()
                    print (game_state_manager.current_state)
                    print ("login")

        screen.fill("grey")
        #blit logo
        screen.blit(titleLogo, (screenWidth // 2 - titleLogo.get_width() // 2, screenHeight // 2 - titleLogo.get_height() // 2))

        #blit PressAnyKey
        screen.blit(titleMsg1, titleMsg1rect)

        #blit framerate
        screen.blit(framerate, framerect)

        pg.display.update()

def loginscreen():
    hoverColourUser ="white" 
    hoverColourPW = "white"

    # Define labels
    username_label = font1.render("Username:", True, black)
    password_label = font1.render("Password:", True, black)

  
    # Define login button
    login_button_rect = pg.Rect(screenWidth // 2 - 50, screenHeight // 2 + 80, 100, 30)
    login_text = font1.render("Login", True, black)
    login_text_rect = login_text.get_rect(center=login_button_rect.center)

    # Define instructions
    instructions_text = "Enter your username and password to login"
    instructions = font1.render(instructions_text, True, black)
    instructions_rect = instructions.get_rect(center=(screenWidth // 2, screenHeight // 2 - 80))

    # Set default values for username and password
    username = ""
    password = ""
    userText = font1.render(username, True, black)
    passText = font1.render(password, True, black)
    username_input_rect = userText.get_rect()
    username_input_rect.center = (screenWidth // 2, screenHeight // 2 - 30) # Set center coordinates
    password_input_rect = passText.get_rect()
    password_input_rect.center = (screenWidth // 2, screenHeight // 2+30) # Set center coordinates

# Create white outline rects
    userOutlineRect = username_input_rect.inflate(370, 20) # Inflate rect by 10 pixels on all sides
    passOutlineRect = password_input_rect.inflate(370, 20) # Inflate rect by 10 pixels on all sides


    while True:
        clock.tick(60)
        framerate = font1.render(str(pg.time.get_ticks()), True, black)
        framerect = framerate.get_rect()
        framerect.bottomright = (screenWidth-10, screenHeight-20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEMOTION:
                if userOutlineRect.collidepoint(pg.mouse.get_pos()):
                    hoverColourUser = black
                elif passOutlineRect.collidepoint(pg.mouse.get_pos()):
                    hoverColourPW = black
                else:
                    hoverColourUser = white
                    hoverColourPW = white
                

           

        # Draw the background
        screen.fill(light_grey)

        # Draw the username and password labels
        screen.blit(username_label, (userOutlineRect.left - 120, userOutlineRect.centery - 8))
        screen.blit(password_label, (passOutlineRect.left - 120,passOutlineRect.centery - 8))

        # Draw the username and password input boxes
        pg.draw.rect(screen, hoverColourUser, userOutlineRect, 2)
        pg.draw.rect(screen, hoverColourPW, passOutlineRect, 2)

         # Draw the login button
        pg.draw.rect(screen, "lightblue", login_button_rect)
        screen.blit(login_text, login_text_rect)

        # Draw the instructions
        screen.blit(instructions, instructions_rect)

        #blit framerate
        screen.blit(framerate, framerect)

        pg.display.flip()
    # To-DO, code for loginscreen


pg.init()

#Initialize game state manager and set state = TitleScreen
game_state_manager = GameStateManager()
game_state_manager.change_state(GameState.TITLESCREEN)

#Setup display
screenWidth = 1280
screenHeight = 720
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("FoodGame")

#Define Colours:
black = (0, 0, 0)
white = (255, 255, 255)
light_grey = (200, 200, 200)
hoverColour = white

#Set Fonts
font1 = pg.font.Font(r"fonts\retro.ttf", 20)


#Setup clock
clock = pg.time.Clock()

#Load Media
titleLogo = pg.image.load(r"img\title.png").convert_alpha()

def main():
    game_state_manager.run_state()

main()
        
