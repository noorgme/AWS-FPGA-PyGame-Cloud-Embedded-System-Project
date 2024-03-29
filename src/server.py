import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 8000

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

cn = []
ad = []

currentId = "0"
pos = ["0:0", "1:0"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                # arr = reply.split(":")
                # id = int(arr[0])
                # val = arr[1]
                # pos[id] = reply

                # if id == 0: nid = 1
                # if id == 1: nid = 0

                #reply = str(nid)+":"+val #pos[nid][:]
                print("Sending: No.: ", len(ad), "asd " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    cn.append(conn)
    ad.append(addr)
    print("Connected to: ", addr)
    print("NUMBER of Connections: ", len(ad))

    start_new_thread(threaded_client, (conn,))