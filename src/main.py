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
    PLAYERCONNECT = 2
    CHARACTERSELECT = 3

    #TO-DO: Implement remaining game states

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
        elif self.current_state == GameState.PLAYERCONNECT:
            playerconnect()
        elif self.current_state == GameState.CHARACTERSELECT:
            characterselect()


#Define Screen Functions


def titlescreen():

    
    titleMsg1 = font1.render("Press any key to continue", True,white)
    titleMsg1rect = titleMsg1.get_rect()
    titleMsg1rect.center = ((screenWidth // 2) + 30, screenHeight //2 + 60)

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
                game_state_manager.change_state(GameState.LOGINSCREEN)
                game_state_manager.run_state()


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
    username_input_rect = pg.Rect((screenWidth // 2) - 100, screenHeight // 2 - 30, 200, 30)
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
    usernameSelected = False
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

            elif event.type == pg.MOUSEBUTTONUP:
                if (username_input_rect.collidepoint(pg.mouse.get_pos())):
                    usernameSelected = True
                    pwSelected = False
                    hoverColourPW = white
                    hoverColourUser = black

                elif (password_input_rect.collidepoint(pg.mouse.get_pos())):
                    pwSelected = True
                    usernameSelected = False
                    hoverColourUser = white
                    hoverColourPW = black

                elif (login_button_rect.collidepoint(pg.mouse.get_pos())):
                    if username == "user" and password == "pass" or 1:
                        game_state_manager.change_state(GameState.PLAYERCONNECT)
                        game_state_manager.run_state()
                else:
                    usernameSelected = False
                    pwSelected = False
                    hoverColourUser = white
                    hoverColourPW = white

            elif event.type == pg.MOUSEMOTION:
                if username_input_rect.collidepoint(pg.mouse.get_pos()) or usernameSelected: #if user hovered or selected 
                    hoverColourUser = black
                    if password_input_rect.collidepoint(pg.mouse.get_pos()) or pwSelected:
                        hoverColourPW = black
                    else:
                        hoverColourPW = white

            
                elif password_input_rect.collidepoint(pg.mouse.get_pos()) or pwSelected:
                    hoverColourPW = black
                    if not usernameSelected:
                        hoverColourUser = white

                else:
                    usernameSelected = False
                    pwSelected = False
                    hoverColourUser = white
                    hoverColourPW = white 

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
                        password = password[:len(password)-1]
                        passtext = font1.render(password, True, black)



       

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

def playerconnect():
    waiting_msg = font1.render('Waiting for players to connect...', True, black)
    start_msg = font1.render('Start game', True, black)
    start_msg_rect = start_msg.get_rect()
    start_msg_rect.center = ((screenWidth / 2 - start_msg.get_width() / 2), (screenHeight - 45))
    
    
    de10 = pg.image.load("img/de10.png").convert_alpha()
    de10 = pg.transform.scale(de10, (300, 150))
    de10_trans = de10.copy()
    de10_trans.set_alpha(120)

    de10rect = de10.get_rect()

    

    # Define square dimensions and spacing
    square_size = 220
    square_spacing = 70

    # Define square coordinates
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
                  (squares[5][0] +125, squares[5][1]+110)]
    numPlayers = 3


    pg.display.flip()
    
    while True:
        screen.fill(light_grey)
        clock.tick(60)
        framerate = font1.render(str(pg.time.get_ticks()), True, black)
        framerect = framerate.get_rect()
        framerect.bottomright = (screenWidth-10, screenHeight-20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONUP:
                if (start_msg_rect.collidepoint(pg.mouse.get_pos())):
                    game_state_manager.change_state(GameState.CHARACTERSELECT)
                    game_state_manager.run_state()
                

            # Draw waiting message and start button
        screen.blit(waiting_msg, (screenWidth / 2 - waiting_msg.get_width() / 2, screenHeight - 100))
        pg.draw.rect(screen, green, (screenWidth / 2 - 75, screenHeight - 60, 150, 50), border_radius=10)
        screen.blit(start_msg, (screenWidth / 2 - start_msg.get_width() / 2, screenHeight - 45))

        # Draw connected message
        connected_msg = font1.render('Players Connected (3-6): '+str(numPlayers), True, black)
        screen.blit(connected_msg, (squares[3][0] - 60, 50))

        # Draw waiting message and start button
        screen.blit(waiting_msg, (screenWidth / 2 - waiting_msg.get_width() / 2, screenHeight - 100))
        pg.draw.rect(screen, green, (screenWidth / 2 - 75, screenHeight - 60, 150, 50), border_radius=10)
        screen.blit(start_msg, (screenWidth / 2 - start_msg.get_width() / 2, screenHeight - 45))
        # Draw connected message
        screen.blit(connected_msg, (squares[3][0] - 60, 50))
        
        #draw squares
        for square in squares:
            pg.draw.rect(screen, blue, (square[0], square[1], square_size, square_size), border_radius=10)
        
        for i in range(0,numPlayers):
            de10rect.center = niosCoords[i]
            screen.blit(de10, de10rect)
        
        for i in range(0, 6-numPlayers):
            de10rect.center = niosCoords[5-i]
            screen.blit(de10_trans, de10rect)
        #blit framerate
        screen.blit(framerate, framerect)
        pg.display.flip()

def characterselect():
   
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        screen.fill(light_grey)
        pg.display.flip()
        
        


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