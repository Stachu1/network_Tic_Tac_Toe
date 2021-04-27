import pygame
import socket
import sys
import time

class Game:

    def __init__(self, network):
        self.network = network
        self.width = 600
        self.height = 500
        self.screen = pygame.display.set_mode((self.width ,self.height))
        self.title = pygame.display.set_caption("Tic_Tac_Toe")
        self.bg = pygame.image.load("Tekstury/BG.png")
        self.x = pygame.image.load("Tekstury/X.png")
        self.o = pygame.image.load("Tekstury/O.png")
        self.up = pygame.image.load("Tekstury/arrow_up.png")
        self.down = pygame.image.load("Tekstury/arrow_down.png")
        self.pos = [(20,20), (186,20), (352,20),
                    (20,186), (186,186), (352,186),
                    (20,352), (186,352), (352,352),]


    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            self.screen.blit(self.bg, (0, 0))
            self.title = pygame.display.set_caption("Tic_Tac_Toe")

            self.move = -1

            if pygame.mouse.get_pressed()[0]:
                self.mouse_pos = [0,0]
                self.mouse_pos[0] = pygame.mouse.get_pos()[0]
                self.mouse_pos[1] = pygame.mouse.get_pos()[1]

                if self.mouse_pos[0] > 495:
                    self.mouse_pos[0] = 495
                if self.mouse_pos[1] > 495:
                    self.mouse_pos[1] = 495

                self.move = round(self.mouse_pos[0] / 165 - 0.5) + (round(self.mouse_pos[1] / 165 - 0.5) * 3)



            reply = network.send(str(self.move) + ":" + str(network.key))

            if int(reply.split(":")[9]) == network.id:
                self.screen.blit(self.down, (500, 175))
            else:
                self.screen.blit(self.up, (500, 175))

            for i in range(9):
                if int(reply.split(":")[i]) == 1:
                    self.screen.blit(self.o, self.pos[i])

            for i in range(9):
                if int(reply.split(":")[i]) == 2:
                    self.screen.blit(self.x, self.pos[i])



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False



            pygame.display.flip()

        pygame.quit()

class Network:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (host, port)
        self.id, self.key = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        identity = self.client.recv(2048).decode()
        print(f"identity:{identity}")
        arr = identity.split(":")
        arr[0] = int(arr[0])
        arr[1] = int(arr[1])
        return arr[0], arr[1]

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)


if __name__ == '__main__':
    try:
        server = sys.argv[1]
        port = int(sys.argv[2])
    except:
        print("Starting on config")

    f = open("config", "r").read().split(":")
    server = f[0]
    port = int(f[1])


    network = Network(server, port)
    game = Game(network)
    game.run()