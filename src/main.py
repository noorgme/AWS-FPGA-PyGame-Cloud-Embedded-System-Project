import pygame as pg
from enum import Enum
from sys import exit
from net_thread import Network
import threading
import time
import os
# from ser_thread import get_connection


#Set working directory
proj_folder = str(os.path.dirname((os.path.dirname(os.path.realpath(__file__)))))
os.chdir(proj_folder+"/include")


net = Network()
user_count = 1
user_count_loop = True

# net.get_connection()
# user_id = net.receive_data()

player_id = 0
host_player = 0
players = []
get_players_loop = False


def get_users_count():
    global user_count
    global user_count_loop
    global get_players_loop
    global players
    if user_count_loop:
        while user_count_loop:
            net.get_connection()
            data = net.receive_data()
            print("Run usr count")

            try:
                if "user_count" in data:
                    user_count = data[-1]
                print(f"Running... user count: {user_count}")    
            except: pass
        
            time.sleep(3)
    elif get_players_loop:
        while get_players_loop:
            net.get_usd()
            data = net.receive_data()
            print("Get Players")

            try:
                if data:
                    players = data
                print(f"Running... player: {players}")    
            except: pass
        
            time.sleep(3)


# user_count_thread = threading.Thread(target=get_users_count)
# user_count_thread.daemon = True  # allow the program to exit if this thread is still running
# user_count_thread.start()


# def get_no_users():
#     global players
#     global get_players_loop
#     while get_players_loop:
#         players = net.get_usr()
#         time.sleep(3)




    




#define game states
class GameState(Enum):
    TITLESCREEN = 0
    LOGINSCREEN = 1
    PLAYERCONNECT = 2
    CHARACTERSELECT = 3
    MAINGAME = 4
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
        elif self.current_state == GameState.MAINGAME:
            maingame()





#Define player class
class Player:
    def __init__(self, name, character, hasBomb, isAlive, playernum):
        self.name = name
        self.character = None
        self.hasBomb = hasBomb
        self.isAlive = isAlive
        self.playernum = playernum
        # if self.character:
        #     self.img = pg.image.load("img/"+character+".png").convert_alpha()
        if playernum == 1:
            playerpos = (screenWidth//2, screenHeight//2+200)
        if playernum == 2:
            playerpos = (screenWidth//2 - 200, screenHeight//2-100)
        if playernum == 3:
            playerpos = (screenWidth//2+200, screenHeight//2-100)
        # self.img = pg.transform.scale(self.img, (150, 150))
        # self.player_rect = self.img.get_rect(center = playerpos)
    
    def throwBomb(self, Player):
        print ("Bomb thrown to " + str(Player.playernum))
        self.hasBomb = False
        Player.hasBomb = True

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


login_reply_var = threading.Event()


def username_thread(net, username, password):
    login_reply = net.send_pass(username, password)
    # Store the login reply in a shared variable
    login_reply_var.set(login_reply)


# network_thread = threading.Thread(target=username_thread, args=(net, username, password))
# network_thread.daemon = True  # allow the program to exit if this thread is still running
# network_thread.start()
# print("Network thread started")




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
    global player_id, host_player
    
    # Create a variable to store the login reply
    

    # Start the network thread
 


    while True:
        clock.tick(60)
        print("Login Screen")
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
                    print("Login button pressed")
                    login_reply = net.send_pass(username,password)
                    while not login_reply:
                        print("paused")
                        pg.time.wait(1)

                    # login_reply = login_reply_var.get()
                    if "Success" in login_reply:
                        player_id = int(login_reply[-1])
                        host_player = Player(username,None, False, True, player_id)
                        if player_id == 1:
                            host_player.hasBomb = True

                        print("username: " + username + "password: " + password)
                        game_state_manager.change_state(GameState.PLAYERCONNECT)
                        game_state_manager.run_state()

                    print(login_reply)
                    print("Player id is " + str(player_id))
                    # if pas == "Success": pass
                    # else: print("Incorrect password")
                    
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
    
    
    


    pg.display.flip()
    global user_count_loop
    global user_count

    
    


    # b = net.get_connection()
    # a = net.receive_data()
    #print("COnn" + str(a))
    
    while True:
      
        screen.fill(light_grey)
        clock.tick(60)
        numPlayers = int(user_count)
        framerate = font1.render(str(pg.time.get_ticks()), True, black)
        framerect = framerate.get_rect()
        framerect.bottomright = (screenWidth-10, screenHeight-20)
        #user_count_thread
        # if user_count != "":
        #     print(user_count)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONUP:
                if (start_msg_rect.collidepoint(pg.mouse.get_pos())):
                    user_count_loop = False
                    game_state_manager.change_state(GameState.CHARACTERSELECT)
                    game_state_manager.run_state()
                

            # Draw waiting message and start button
        screen.blit(waiting_msg, (screenWidth / 2 - waiting_msg.get_width() / 2, screenHeight - 100))
        pg.draw.rect(screen, green, (screenWidth / 2 - 75, screenHeight - 60, 150, 50), border_radius=10)
        screen.blit(start_msg, (screenWidth / 2 - start_msg.get_width() / 2, screenHeight - 45))

        # Draw connected message
        
        #print("Connection:" + str(a))

        # print(user_count)
        # a = net.receive_data()




        connected_msg = font1.render(f'Players Connected (3-6): {user_count}', True, black)
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
        print("getting No of Users: ")
        # get_users_count()
        try:
            user_count = net.get_connection()
            print("got users", user_count)
        except:
            print("waiting for users")
            # pg.game.wait(100)
            
        #b = net.get_connection()

        # a = net.receive_data()
        # try:
      # except:
        #     pass  #     a = net.receive_data()
        

# def characterselect():
   
#     pg.display.flip()

#     while True:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 pg.quit()
#                 exit()

#         screen.fill(light_grey)
#         pg.display.flip()

# net2 = Network()

whoSelecting = 0

# def get_char_select():
#     global whoSelecting
#     while True:

#         net2.char_select()
        
#         try:
#             a = net2.receive_data()
#             if "char_select:" in a:
#                 whoSelecting = int(a[-1])
#         except:
#             pass

#         time.sleep(3)


# player_count_thread = threading.Thread(target=get_char_select)
# player_count_thread.daemon = True  # allow the program to exit if this thread is still running
# player_count_thread.start()


# play = ""




def characterselect():
    #  #load character images
    # characters = ["sarim", "bouganis", "naylor"]
    # player1 = Player("noor", characters[0], hasBomb = True, isAlive = True, playernum = 1)
    # player2 = Player("shaheer", characters[1], hasBomb = False, isAlive = True, playernum =  2)
    # player3 = Player("jim", characters[2], hasBomb = False, isAlive = True, playernum = 3)
    # player1 = pg.image.load("img/sarim.png").convert_alpha()
    # player2 = pg.image.load("img/sarim.png").convert_alpha()
    # player3 = pg.image.load("img/sarim.png").convert_alpha()
    # players = [player1, player2, player3]

    
    global play

    

    characters_1 = pg.image.load("img/sarim.png").convert_alpha()
    characters_2 = pg.image.load("img/bouganis.png").convert_alpha()
    characters_3 = pg.image.load("img/naylor.png").convert_alpha()

    characters_1 = pg.transform.scale(characters_1, (300, 150))
    characters_1_trans = characters_1.copy()
    characters_1_trans.set_alpha(240)#Pass 0 for invisible and 255 for fully opaque.
    characters_1rect = characters_1.get_rect(center=((screenWidth // 3)-250,(screenHeight // 3)-70))

    characters_2 = pg.transform.scale(characters_2, (300, 150))
    characters_2_trans = characters_2.copy()
    characters_2_trans.set_alpha(240)
    characters_2rect = characters_2.get_rect(center=((screenWidth // 2), (screenHeight // 3)-70))

    characters_3 = pg.transform.scale(characters_3, (300, 150))
    characters_3_trans = characters_3.copy()
    characters_3_trans.set_alpha(240)
    characters_3rect = characters_3.get_rect(center=((screenWidth // 1.5)+250,(screenHeight // 3)-70))
    
    waiting_msg1 = font1.render("Character Select", True, black)
    waiting_msg1rect =  waiting_msg1.get_rect(center= ((screenWidth // 2) , (screenHeight //3) -200))        

    # global success_msg
    # global success_msgrect
    
    charsSelected=0
    global whoSelecting
    pg.display.flip()
    global hostID
    global get_players_loop, user_count_loop
    user_count_loop = False
    hostID = host_player.playernum
    get_players_loop = True

  

    # try:
    #     play = net.get_usr().split(",")
    # except:
    #     play = net.get_usr()
    #     numPlayers = 1
    print("getting users: ")
    play = net.get_usr()
    numPlayers = 1

    if "," in play:
        play = play.split(",")
        numPlayers = len(play)
    else: play = [play]
    
    global whoSelecting

    # whoSelecting = 0

    print("jnj ",play)
    
    print("User ID:", player_id)
    print("sad:", numPlayers)

  
    # time.sleep(0.5)
    print("Kul Khara")
    try:
        selected_char = net.recieve_char()
    except:
        selected_char = []

    try:
        whoSelecting = net.char_select()
    except:
        whoSelecting = 0
    
    
    

    


    # selected_char = []

    while True:
        print("Starting Lopp")

        
        screen.fill(light_grey)
        screen.blit(characters_1_trans, characters_1rect)
        screen.blit(characters_2_trans, characters_2rect)
        screen.blit(characters_3_trans, characters_3rect)
        screen.blit(waiting_msg1, waiting_msg1rect)
        pg.display.flip()
        print("Char: ", charsSelected , " Num: ", numPlayers)
        while charsSelected < numPlayers:
            print("Running")
            screen.fill(light_grey)
            screen.blit(characters_1_trans, characters_1rect)
            screen.blit(characters_2_trans, characters_2rect)
            screen.blit(characters_3_trans, characters_3rect)
            screen.blit(waiting_msg1, waiting_msg1rect)
            #config and blit whos turn it is message
            Plays_msg = font1.render(play[whoSelecting]+' please connect to a character', True, black)
            Plays_msgrect = Plays_msg.get_rect(center=((screenWidth // 2) , (screenHeight //2) +150))
            #screen.blit(Plays_msg,Plays_msgrect)

            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if whoSelecting != player_id:#i am not selecting

                    # if ["""(NEW whoSelecting value from DB) != whoSelecting (current whoSelecting value)"""]: #TO-DO
                    #     #TO-DO ANOTHER PLAYER HAS SELECTED! APPEND WHO THEY SELECTED IN A SELECTED CHARACTERS ARRAY, THEN UPDATE whoSelected variable
                        
                    #     success_msg = font1.render(play[whoSelecting]+' has chosen a' + """selectedCharactersArray[-1]""", True, black) #TO-DO: SELECTED CHARACTER
                    # else:

                    success_msg = font1.render(play[whoSelecting]+' is choosing a character', True, black)
                    #GET WHAT CHARACTERSS SELECTED FROM DB
                    
                    success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))

                    
                    screen.blit(success_msg,success_msgrect)
                    try:
                        whoSelecting = net.char_select()
                    except:
                        pass

                else:
                    success_msg = font1.render('Please choose a character', True, black)#my turn to select character

                    success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                    screen.blit(success_msg,success_msgrect)

                    if (event.type == pg.MOUSEBUTTONUP): 
                        

                        if characters_1rect.collidepoint(pg.mouse.get_pos()): 
                            if "sarim" not in selected_char: # TO-DO: CHECK IF CHARACTER IS ALREADY IN SELECTED CHARACTERS ARRAY
                                host_player.character = "sarim"
                                success_msg = font1.render(play[whoSelecting]+' selected Prof Baig', True, black)
                                charsSelected += 1
                                try:
                                    selected_char = net.recieve_char(host_player.character)
                                except:
                                    pass

                                success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                                screen.blit(success_msg,success_msgrect)

                            else:
                                success_msg = font1.render("Character selected, please select another one", True, black)
                            ##TO DO: SEND CHARACTER SLECTED TO SERVER, DB SHOULD UPDATE THE PLAYERS CHARACTER AND SENDBACK INCREMENTED "WHOSELECTED" AND "WHICH CHARACTERS SELECTED"
                            success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                            screen.blit(success_msg,success_msgrect)    

                        elif characters_2rect.collidepoint(pg.mouse.get_pos()): #TO-DO: AND CHARACTER NOT ALREADY SELECTED
                            if "bouganis" not in selected_char:
                                host_player.character = "bouganis"
                                success_msg = font1.render(play[whoSelecting]+'selected Prof Bouganis', True, black)
                                charsSelected += 1
                                try:
                                    selected_char = net.recieve_char(host_player.character)
                                except:
                                    pass

                                success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                                screen.blit(success_msg,success_msgrect)
                            
                        
                            else:
                                success_msg = font1.render("Character selected, please select another one", True, black)
                            ##TO DO: SEND CHARACTER SLECTED TO SERVER, DB SHOULD UPDATE THE PLAYERS CHARACTER AND SENDBACK INCREMENTED "WHOSELECTED" AND "WHICH CHARACTERS SELECTED"
                            success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                            screen.blit(success_msg,success_msgrect) 
                            
                            ##TO DO: SEND CHARACTER SLECTED TO SERVER, DB SHOULD UPDATE THE PLAYERS CHARACTER AND SENDBACK INCREMENTED "WHOSELECTED" AND "WHICH CHARACTERS SELECTED"
                        elif characters_2rect.collidepoint(pg.mouse.get_pos()): #TO-DO: AND CHARACTER NOT ALREADY SELECTED
                            if "naylor" not in selected_char:
                                host_player.character = "naylor"
                                success_msg = font1.render(play[whoSelecting]+'selected Prof Naylor', True, black)
                                charsSelected += 1
                                try:
                                    selected_char = net.recieve_char(host_player.character)
                                except:
                                    pass

                                success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                                screen.blit(success_msg,success_msgrect)

                            else:
                                success_msg = font1.render("Character selected, please select another one", True, black)
                            ##TO DO: SEND CHARACTER SLECTED TO SERVER, DB SHOULD UPDATE THE PLAYERS CHARACTER AND SENDBACK INCREMENTED "WHOSELECTED" AND "WHICH CHARACTERS SELECTED"
                            success_msgrect = success_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                            screen.blit(success_msg,success_msgrect) 
                       
                    
                        ##TO DO: SEND CHARACTER SLECTED TO SERVER, DB SHOULD UPDATE THE PLAYERS CHARACTER AND SENDBACK INCREMENTED "WHOSELECTED" AND "WHICH CHARACTERS SELECTED"
                
                pg.display.flip()         

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.KEYDOWN:
                player_count_thread = False
                game_state_manager.change_state(GameState.MAINGAME)
                game_state_manager.run_state()


        #blit startgame prompt
        start_msg = font1.render('Press any key to start game', True, black)
        start_msg_rect = start_msg.get_rect()
        start_msg_rect.center = ((screenWidth / 2 - start_msg.get_width() / 2), (screenHeight - 45))
        screen.blit(start_msg, (screenWidth / 2 - start_msg.get_width() / 2, (screenHeight//2) +50))

        

        #draw button?
        pg.draw.rect(screen, green, (screenWidth / 2 -190, (screenHeight //2) +40, 365, 50), border_radius=10)
        
        #screen.blit(Plays_msg,Plays_msgrect)
        
      
      
 
        pg.display.flip()

c = 0
# net = Network()

# def send_data(c):
#         """
#         Send position to server
#         :return: None
#         """
#         data = str(net.id) + ":" + str(c)
#         reply = net.send(data)
#         return reply

# # @staticmethod
# def parse_data(data):
#         try:
#             d = data.split(":")[1]
#             return int(d[1])
#         except:
#             return 0



def maingame():
    global host_player
    global play, c
    pg.display.flip()
    #load character images

    


    #load bomb
    bomb_img = pg.image.load("img/bomb.png").convert_alpha()
    bomb_img = pg.transform.scale(bomb_img, (70, 70))
    bomb_rect = bomb_img.get_rect()
    # fps=30
    clock = pg.time.Clock()
    hasBomb = 1 #to-do GET hasBomb value from server. Should start at 1 meaning player with ID 1 has bomb at the starT
        
    while True:
            clock.tick(60)
            initial = players[c]
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        c+=1
                        if c>=len(players):
                            c = 0

                        print("Left")
                    elif event.key == pg.K_RIGHT:

                        print(c,"RIGHT")

            if hasBomb == host_player.playernum:
                pass #I HAVE THE MFCKIN BOMB

            initial.hasBomb = False
            # d = parse_data(send_data(c))
            # print(send_data(c))
            players[c].hasBomb = True

            screen.fill("orange")
            screen.blit(player1.img, player1.player_rect)
            screen.blit(player2.img, player2.player_rect)
            screen.blit(player3.img, player3.player_rect)

            
            


            for player in players:
                if (player.hasBomb):
                    #initial = player
                    
                    bomb_rect.center = (player.player_rect[0]+140, player.player_rect[1]+100) 
                    screen.blit(bomb_img, bomb_rect)
        
            
            #pg.display.flip()
                
            pg.display.update()
            #fpsclock.tick(fps)




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
font1 = pg.font.Font(r"fonts/retro.ttf", 20)


#Setup clock
clock = pg.time.Clock()

#Load Media
titleLogo = pg.image.load(r"img/title.png").convert_alpha()


def main():
    game_state_manager.run_state()

main()