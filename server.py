import socket, sys
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 23456
server_ip = "192.168.0.7"
print(server_ip)

try:
    s.bind((server_ip, port))

except socket.error as e:
    print(str(e))

s.listen(3)
print("Waiting for players...")

currentID = "0"
pos = ["0:50, 50", "1:100, 100"]

def threaded_client(conn):
    global currentID, pos
    conn.send(str.encode(currentID))
    currentID = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(1024)
            reply = data.decode("utf-8")
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: "+reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending :"+reply)
            
            conn.sendall(str.encode(reply))
        
        except:
            break
    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to :",addr)

    start_new_thread(threaded_client, (conn,))
 