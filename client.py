import pygame
from network import Network
from player import Player

WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


def redraw_window(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        p.move()
        redraw_window(win, p, p2)


if __name__ == "__main__":
    main()