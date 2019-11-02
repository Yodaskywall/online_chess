import socket
from game import Game
from _thread import *
import pickle
HEADERSIZE = 10


def pickle_send(conn, object):
    msg = pickle.dumps(object)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    conn.send(msg)


def pickle_receive(conn):
    full_msg = b''
    new_msg = True
    while True:
        msg = conn.recv(16)

        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            object = pickle.loads(full_msg[HEADERSIZE:])
            return object

server = "192.168.1.108"
port = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(2096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break

                else:
                    if data == "reset":
                        game.reset()

                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    pickle_send(conn, reply)

            else:
                break

        except Exception as e:
            print(e)

    print("Lost connection")
    try:
        del games[gameId]
        print(f"Closing Game {gameId}.")

    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")

    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
