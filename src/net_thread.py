import socket
import threading
import sys
import json
import time
import ast
# create a socket object



char_selected = []

class Network:
    def __init__(self):
          self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          # get local machine nam
          self.host = "3.85.175.1"
          # set port numbe
          self.port = 9991
          # connect to the serve
          self.clientsocket.connect((self.host, self.port))
        #   self.receive_thread = threading.Thread(target=self.receive_data)
        #   self.receive_thread.start()
          # function to handle receiving data from the server
    def receive_data(self):
        # while True:
        #     try:
                # receive data from server
                try:
                    data = self.clientsocket.recv(2048).decode("utf-8")
                    # print("b"+data)
                    # if not data:
                    #     break
                # if "Client:" in data:
                #     print(data)
                #     continue

                # decode and print the data
                    # print(data)   
                    return data
                except socket.timeout:
                    print("timeout")
                
                #return data.decode('utf-8')
        #     except:
        #         break
        # # print("Connection Closed")
        # clientsocket.close()
            

    # create a new thread to handle receiving data from the server
    

    def get_connection(self):
        self.clientsocket.send(str.encode("Clients:"))
        time.sleep(0.1)
        try:
            reply = self.clientsocket.recv(2048).decode("utf-8")
            if "user_count:" in reply:
                 reply = reply[-1]
        except:
            reply = ""

        return reply

    # send data to the server
    def send_data(self,data):
        try:
                self.clientsocket.send(str.encode(data))
                return 0
                # reply = clientsocket.recv(2048).decode()
                # return reply
        except socket.error as e:
                return str(e)
        


    def send_pass(self, username, password):
        # data = "login:"+username + "," + password
        data = {"username": username, "password": password}
        data = json.dumps(data)

        self.clientsocket.sendall(bytes(data,encoding="utf-8"))
        time.sleep(0.3)
        try:
            reply = self.clientsocket.recv(2048).decode("utf-8")
        except:
            reply = ""
        return reply

    def get_usr(self):
        self.clientsocket.send(str.encode("get_usr:"))
        time.sleep(0.3)
        try:
            reply = self.clientsocket.recv(2048).decode("utf-8")
            if "usr" in reply:
                reply = reply.split(":")
                try:
                    reply = reply[1]
                except:
                    reply = ""
        except:
             reply = ""
        #reply = self.clientsocket.recv(2048).decode("utf-8")
        return reply

    def char_select(self):
        self.clientsocket.send(str.encode("char_select:"))
        time.sleep(0.1)
        reply = self.clientsocket.recv(2048).decode("utf-8")
        try:
            reply = reply.split(":")
            reply = reply[1]
        except:
            reply = "1"

        return int(reply)

    def recieve_char(self, char=None):
        if char == None:
             char = "Character_Selected:"
        else:
            char = "Character_Selected:" + char
        self.clientsocket.send(str.encode(char))
        time.sleep(0.1)
        b = ''
        try:
            a = self.clientsocket.recv(2048).decode("utf-8")
            print("recieved: ",a)
            a = a.split(":")
            if len(a) > 1:
                b = a[1]
        #     try:
        #         b = a[1].split(",")
        #     except:
        #         b = a
        #         return b
        except:
              pass
        return b
    
    def getReadyPlayers(self, type, playernum):
        if type == "imready":
              self.clientsocket.send(str.encode(type+str(playernum)))
        elif type == "whosReady":
            self.clientsocket.send(str.encode(type))
            time.sleep(0.1)
            try:
                whosReady = ast.literal_eval(self.clientsocket.recv(2048).decode("utf-8"))
            except:
                pass
            return whosReady
    
    def hasbomb(self, player):
        if player != 99:   #tell server who has bomb
            self.clientsocket.send(str.encode("hasBombTell: "+str(player)))
            return None
        else: #ask server who has bomb
            self.clientsocket.send(str.encode("hasBombAsk"))
            
            time.sleep(0.1)
            try:
                
                hasBomb = int(self.clientsocket.recv(2048).decode("utf-8"))
            except:
                print ("failed to communicate")
            
            return hasBomb


    # while True:
    #     # get user input
    #     data = input("Enter: ")

    #     # send the data to the server
    #     #send_data(data)
    #     clientsocket.send(str.encode(data))
        

    #     # if the user types 'exit', close the client
    #     if data == 'exit':
    #         clientsocket.close()
    #         break
    #     #receive_data()