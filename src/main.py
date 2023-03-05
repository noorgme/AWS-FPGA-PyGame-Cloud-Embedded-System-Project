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

    # Define input boxes
    username_input_rect = pg.Rect(screenWidth // 2 - 100, screenHeight // 2 - 30, 200, 30)
    password_input_rect = pg.Rect(screenWidth // 2 - 100, screenHeight // 2 + 30, 200, 30)

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
    usertext = font1.render(username, True, black)
    passtext = font1.render(password, True, black)
    usernameHovered = False
    usernameSelected = False
    pwHovered = False
    pwSelected = False


    while True:
        clock.tick(60)
        framerate = font1.render(str(pg.time.get_ticks()), True, black)
        framerect = framerate.get_rect()
        framerect.bottomright = (screenWidth-10, screenHeight-20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEMOTION:
                if username_input_rect.collidepoint(pg.mouse.get_pos()):
                    hoverColourUser = black
                    usernameHovered = True

                else:
                    usernameHovered = False
                    if (usernameSelected):
                        hoverColourUser = black
            
                if password_input_rect.collidepoint(pg.mouse.get_pos()):
                    hoverColourPW = black
                    pwHovered = True
                else:
                    pwHovered = False
                    if (pwSelected):
                        hoverColourPW = black
                    else:
                        hoverColourPW = white

            elif event.type == pg.MOUSEBUTTONUP:
                if (usernameHovered):
                    usernameSelected = True
                else:
                    hoverColourUser = white
                    usernameSelected = False

                if (pwHovered):
                    pwSelected = True
                else:
                    hoverColourUser = white
                    pwSelected = False
            elif event.type == pg.KEYDOWN:
                if (usernameSelected):
                    if event.unicode.isalnum():
                        if len(username) < 14:
                            username += event.unicode
                            usertext = font1.render(username, True, black)
                    elif event.key == pg.K_BACKSPACE:
                        username = username[:len(username)-1]
                        usertext = font1.render(username, True, black)
                elif (pwSelected):
                    if event.unicode.isalnum():
                        if len(password) < 14:
                            password += event.unicode
                            passtext = font1.render(password, True, black)
                    elif event.key == pg.K_BACKSPACE:
                        password = username[:len(username)-1]
                        passtext = font1.render(username, True, black)                    


           

        # Draw the background
        screen.fill(light_grey)

        # Draw the username and password labels
        screen.blit(username_label, (username_input_rect.left - 120, username_input_rect.centery - 8))
        screen.blit(password_label, (password_input_rect.left - 120, password_input_rect.centery - 8))

        # Draw the username and password input boxes
        pg.draw.rect(screen, hoverColourUser, username_input_rect, 2)
        pg.draw.rect(screen, hoverColourPW, password_input_rect, 2)

         # Draw the login button
        pg.draw.rect(screen, "lightblue", login_button_rect)
        screen.blit(login_text, login_text_rect)

        # Draw the instructions
        screen.blit(instructions, instructions_rect)
        screen.blit(usertext,  (username_input_rect.left+8, username_input_rect.centery-13)) 
        screen.blit(passtext,  (username_input_rect.left+8, username_input_rect.centery+47)) 
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