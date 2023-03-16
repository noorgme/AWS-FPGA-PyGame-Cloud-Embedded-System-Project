import socket
import threading

# create a socket object

class Network:
    def __init__(self):
          self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          # get local machine nam
          self.host = socket.gethostname()
          # set port numbe
          self.port = 9990
          # connect to the serve
          self.clientsocket.connect((self.host, self.port))
          self.receive_thread = threading.Thread(target=self.receive_data)
          self.receive_thread.start()
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
                    print(data)   
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
        return 0

    # send data to the server
    def send_data(self,data):
        try:
                self.clientsocket.send(str.encode(data))
                return 0
                # reply = clientsocket.recv(2048).decode()
                # return reply
        except socket.error as e:
                return str(e)


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