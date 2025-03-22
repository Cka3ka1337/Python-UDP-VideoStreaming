import logging
import time

import pygame

from scripts.client import Client


def main():
    pygame.init()
    logging.basicConfig(format='[%(name)s] (%(asctime)s) - %(message)s', level=logging.NOTSET, datefmt='%H:%M:%S')
    
    sc = pygame.display.set_mode((1920 // 2, 1200 // 2))
    clock = pygame.time.Clock()

    client = Client(('127.0.0.1', 40000))
    client.connect()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        sc.blit(
            client.frame,
            (0, 0)
        )
            
        print(time.time())
        pygame.display.update()
        clock.tick(128)


if __name__ == '__main__':
    main()