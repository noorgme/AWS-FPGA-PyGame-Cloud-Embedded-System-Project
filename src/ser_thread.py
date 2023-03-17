import socket
import threading
import json
# from adding_player import put_player



# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set port number
port = 9991
# bind the socket to a public host and a port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(5)

print('Server listening...')

# list to keep track of connected clients
clients = []

users = []


def handle_client(clientsocket, addr):
    print('Got a connection from %s' % str(addr))

    # add the client socket to the list of clients
    clients.append(clientsocket)
    a = len(clients)
    g = False

    try:
        while True:
            # receive data from client
            data = clientsocket.recv(2048).decode("utf-8")
            if not data:
                clientsocket.send(str.encode("Goodbye"))
                break
            if "Clients:" in data:
            #     g = True
            # if g:
                a = len(clients)
                num = "user_count:" + str(a)
                print(num)
                for client in clients:
                    client.send(num.encode("utf-8"))

            # print(("Received: %s", json.loads(data)))

            if "get_usr:" in data:
                users_str = ','.join(users) # Convert the list to a comma-separated string
                client.send(users_str.encode('utf-8'))
                #client.send(users.encode("utf-8"))

            if "{" in data:  # check if data is not empty
                try:
                    decoded_data = json.loads(data)
                    print("Received:", decoded_data)
                    print("Received:", decoded_data['username'])
                    user =  decoded_data['username']
                    password = decoded_data['password']
                    #response = put_player(user, password)
                    response = "Success"
                    if response == "Success":
                        users.append(user)
                    player_id = users.index(user) + 1
                    response = response + ":" + str(player_id)
                    client.send(response.encode("utf-8"))


                    # relay the message to all other connected clients
                    # for client in clients:
                    #     if client != clientsocket:
                    #         try:
                    #             client.send(data.encode("utf-8"))
                    #         except socket.error:
                    #             print('Error sending message to client')
                    #             clients.remove(client)
                    #             client.close()
                except json.decoder.JSONDecodeError:
                    print('Invalid JSON received from client')
                    continue
            else:
                print('Empty message received from client')


            # relay the message to all other connected clients
            # for client in clients:
            #     if client != clientsocket:
            #         try:
            #             client.send(data.encode("utf-8"))
            #         except socket.error:
            #             print('Error sending message to client')
            #             clients.remove(client)
            #             client.close()
    except KeyboardInterrupt:
        print('Server shutting down...')
    finally:
        # remove the client socket from the list of clients
        clients.remove(clientsocket)
        clientsocket.close()
        print('Connection closed for client %s' % str(addr))


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
