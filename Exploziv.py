import pygame
from pygame.locals import *
from bin.globals import EventHandler, InputBox
from bin.board import Board
from bin.board import ChessHandler
import bin.settings as settings
import asyncio
# --
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Chess')
# --
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

# Create Background
background_image = pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert()
background_image = pygame.transform.scale(background_image, (600,600))
# Create the board and all the pieces
board=Board()
# Pygame loop
async def main():
    input_box = InputBox(100, 100, 140, 32)
    while True:

        for event in pygame.event.get():
            EventHandler(event, board)
            input_box.handle_event(event, board)

        screen.blit(background_image, [0,0])
        board.commit(screen)
        input_box.draw(screen)
        # --
        pygame.display.flip()
        clock.tick(settings.TICK_RATE)

asyncio.run(main())
