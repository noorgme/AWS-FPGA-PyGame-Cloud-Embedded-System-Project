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
    characters_1rect = characters_1.get_rect(center=((screenWidth // 3)-250,(screenHeight // 3)-70))

    characters_2 = pg.transform.scale(characters_2, (300, 150))
    characters_2_trans = characters_2.copy()
    characters_2_trans.set_alpha(240)
    characters_2rect = characters_2.get_rect(center=((screenWidth // 2), (screenHeight // 3)-70))

    characters_3 = pg.transform.scale(characters_3, (300, 150))
    characters_3_trans = characters_3.copy()
    characters_3_trans.set_alpha(120)
    characters_3rect = characters_3.get_rect(center=((screenWidth // 1.5)+250,(screenHeight // 3)-70))
    
    # for player in players:
    #     player = pg.transform.scale(player, (300, 150))
    play=["jim","noor", "shaheer"]  
    
    waiting_msg2 = font1.render("No Character selected yet", True, black)
    waiting_msg2rect =  waiting_msg2.get_rect(center= ((screenWidth // 2) , (screenHeight //3) -200))

    unsuccess_msg = font1.render("Character selected, please select another one", True, black)
    unsuccess_msgrect = unsuccess_msg.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
    
    numPlayers = 3
    
    cc=0
    ccc1=0
    ccc2=0
    ccc3=0
    pg.display.flip()
    characters_rects=[characters_1rect,characters_2rect, characters_3rect]
    #characters_rects=[]
    
    while True:
        for event in pg.event.get():
            state = "Waiting"
            if cc < numPlayers:
               plays = play[cc]
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONUP:
                if cc <numPlayers:
                    print(cc)
                    #plays = play[cc]
                    state = "0"
                    Plays_msg = font1.render(' please connect to a character'+plays, True, black)
                    Plays_msgrect = Plays_msg.get_rect(center=((screenWidth // 2) , (screenHeight //2) +150))
                    #screen.blit(Plays_msg,Plays_msgrect)
                    print (plays)
                    if (characters_1rect.collidepoint(pg.mouse.get_pos())) and ccc1<1:
                     #       playersss.append(player)
                        state ="1"
                        #characters_rects.append(characters_1rect)
                        success_msg1 = font1.render(plays+' connected to Character1', True, black)
                        success_msg1rect = success_msg1.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +150))
                        ccc1 = ccc1+1
                        cc+=1
                        #print("successfully selected")
                        
                    elif (characters_2rect.collidepoint(pg.mouse.get_pos())) and ccc2<1:
                     #       playersss.append(player)
                        state ="2"
                        #characters_rects.append(characters_2rect)
                        success_msg2 = font1.render(plays+' connected to Character2', True, black)
                        success_msg2rect = success_msg2.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +200))
                        ccc2 = ccc2+1
                        cc+=1
                       # print("successfully selected")
                        
                    elif (characters_3rect.collidepoint(pg.mouse.get_pos())) and ccc3<1:
                     #       playersss.append(player)
                        state ="3"
                       # characters_rects.append(characters_3rect)
                        success_msg3 = font1.render(plays+' connected to Character3', True, black)
                        success_msg3rect = success_msg3.get_rect(center= ((screenWidth // 2) , (screenHeight //2) +250))
                        ccc3 = ccc3+1
                        cc+=1
                    elif  ((characters_3rect.collidepoint(pg.mouse.get_pos())) and ccc3!=0) or  ((characters_2rect.collidepoint(pg.mouse.get_pos())) and ccc2!=0) or ((characters_1rect.collidepoint(pg.mouse.get_pos())) and ccc1!=0):
                        state ="error"
                        print("error")
            elif ccc3 <1 or ccc2 <1 or ccc1 <1:
                 state = "0"
                 Plays_msg = font1.render(plays+' please connect to a character', True, black)
                 Plays_msgrect = Plays_msg.get_rect(center=((screenWidth // 2) , (screenHeight //2) +150)) 
                
            elif ccc3>0 and ccc2 >0 and ccc1>0:
                state = "All_Characters_Connected"
                
            if event.type == pg.KEYDOWN and state == "All_Characters_Connected":
                game_state_manager.change_state(GameState.LOGINSCREEN)
               # game_state_manager.run_state(MAINGAME)
                #print("game")
                        
                
            screen.fill(light_grey)
            
            start_msg = font1.render('Start game', True, black)
            start_msg_rect = start_msg.get_rect()
            start_msg_rect.center = ((screenWidth / 2 - start_msg.get_width() / 2), (screenHeight - 45))
            waiting_msg2 = font1.render("No Character selected yet. Press any key to start character select", True, black)
            waiting_msg2rect =  waiting_msg2.get_rect(center= ((screenWidth // 2) , (screenHeight //3) -200))        
            if state == "Waiting":
               screen.blit(waiting_msg2,waiting_msg2rect)
            elif state == "All_Characters_Connected" :
               screen.blit(success_msg1,success_msg1rect)
               screen.blit(success_msg2,success_msg2rect)
               screen.blit(success_msg3,success_msg3rect)
               pg.draw.rect(screen, green, (screenWidth / 2 - 75, (screenHeight //2) +40, 150, 50), border_radius=10)
               screen.blit(start_msg, (screenWidth / 2 - start_msg.get_width() / 2, (screenHeight//2) +50))
               print("state_all")
            elif state=="0":
                screen.blit(Plays_msg,Plays_msgrect)
            elif state =="1" :
                screen.blit(success_msg1,success_msg1rect)
            elif state =="2":
               screen.blit(success_msg2,success_msg2rect)
            elif state =="3":
               screen.blit(success_msg3,success_msg3rect)
            elif state =="error":
               screen.blit(unsuccess_msg,unsuccess_msgrect)
      
      
        screen.blit(characters_1,characters_1rect)
        screen.blit(characters_2,characters_2rect)
        screen.blit(characters_3,characters_3rect)
        screen.blit(waiting_msg2,waiting_msg2rect)
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