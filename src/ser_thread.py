import socket
import threading

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set port number
port = 9990
# bind the socket to a public host and a port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(5)

print('Server listening...')

# list to keep track of connected clients
clients = []


# function to handle each client connection
def handle_client(clientsocket, addr):
    print('Got a connection from %s' % str(addr))

    # add the client socket to the list of clients
    clients.append(clientsocket)
    a = len(clients)
    g = False
    


    while True:
        try:
            # receive data from client
            data = clientsocket.recv(2048).decode("utf-8")
            if not data:
                clientsocket.send(str.encode("Goodbye"))
                break
            if "Clients:" in data:
                g = True
            if g:
                
                a = len(clients)
                num = str(a)
                print(num)
                for client in clients:
                    client.send(num.encode("utf-8"))
            
            print(("Received: %s",data))

            # relay the message to all other connected clients
            # print(len(clients))
            # for client in clients:
            #     if client != clientsocket:
            #         print("Sending: " + data)
            #         client.send(data.encode("utf-8"))
        except KeyboardInterrupt:
            # remove the client socket from the list of clients
            clients.remove(clientsocket)
            clientsocket.close()
            return


# def get_connection():
#         data = "Clients:"+ str(len(clients))
#         print(data)
#         return clientsocket.send(data.encode("utf-8"))

# listen for incoming connections from clients
while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    # create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, addr))
    client_thread.start()
    # get_connection()
