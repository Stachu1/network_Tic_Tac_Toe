import socket
from _thread import *
import sys
import random
import time

class Player:
    def __init__(self, id, key):
        self.id = id
        self.key = key


    def encode_identity(self):
        return f"{self.id}:{self.key}"


def turn_key():
    for p in players:
        if p.id == chart[9]:
            return p.key


def threaded_client(conn, player):
    conn.send(str.encode(player.encode_identity()))
    reply = ''

    while True:
        try:
            data = conn.recv(2048)

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                reply = data.decode('utf-8')
                # print("Received: " + reply)

                if int(reply.split(":")[0]) != -1 and int(reply.split(":")[1]) == turn_key():
                    if chart[int(reply.split(":")[0])] == 0:
                        chart[int(reply.split(":")[0])] = chart[9]
                        if chart[9] == 1:
                            chart[9] = 2
                        else:
                            chart[9] = 1

                str_chart = ""
                for i in range(9):
                    str_chart = str_chart + str(chart[i]) + ":"
                message = str_chart + str(chart[9])
                # print("Sending: " + str(message))
                conn.sendall(str.encode(message))

                for j in range(2):
                    i = j+1
                    if chart[0] == i and chart[1] == i and chart[2] == i or chart[3] == i and chart[4] == i and chart[5] == i or chart[6] == i and chart[7] == i and chart[8] == i or chart[0] == i and chart[3] == i and chart[6] == i or chart[1] == i and chart[4] == i and chart[7] == i or chart[2] == i and chart[5] == i and chart[8] == i or chart[0] == i and chart[4] == i and chart[8] == i or chart[2] == i and chart[4] == i and chart[6] == i:
                        time.sleep(3)
                        for i in range(9):
                            chart[i] = 0
                        break

                chart_check = 0
                for i in range(9):
                    if chart[i] != 0:
                        chart_check = chart_check + 1
                if chart_check == 9:
                    time.sleep(3)
                    for i in range(9):
                        chart[i] = 0
        except:
            break
    print("Connection Closed id:", player.id, "key:", player.key)
    Id[player.id - 1] = 0
    for p in players:
        if p.id == player.id:
            players.remove(p)
    conn.close()



server = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection ip: " + str(server_ip) + " port: " + str(port))

Id = [0,0]
currentKey = random.randint(1000, 9999)


players = []


chart = [0,0,0,
         0,0,0,
         0,0,0, 1]

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if Id[0] == 0:
        Id[0] = 1
        currentId = 1
    else:
        if Id[1] == 0:
            Id[1] = 1
            currentId = 2
        else:
            currentId = 0


    player = Player(currentId, currentKey)
    print("Created player id:", currentId, "key:", currentKey)
    players.append(player)

    start_new_thread(threaded_client, (conn,player))
    currentKey = random.randint(1000, 9999)