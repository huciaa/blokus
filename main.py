# Example file showing a circle moving on screen
import pygame
from field import Field, BlockType, Block
from board import Board
from game import PlayerType, Player

from pygame.rect import Rect


# pygame setup
pygame.init()

screen_width = 600
screen_height = 900
cell_size = 30

current_block_to_display = 6
rectangle_draging = False

last_block_x = 999
last_block_y = 999

rotation = 0

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

board = Board(screen=screen)


players: list[Player] = [
    Player(PlayerType.BLUE),
    Player(PlayerType.RED),
    Player(PlayerType.GREEN),
    Player(PlayerType.YELLOW),
]

current_player_number = 0


while running:

    current_player = players[current_player_number]
    current_color = current_player.player_type.color()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block_to_display -= 1
                if current_block_to_display < 0:
                    current_block_to_display = len(blocks) - 1

            if event.key == pygame.K_RIGHT:
                current_block_to_display += 1
                if current_block_to_display >= len(blocks):
                    current_block_to_display = 0

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        board.draw_board()

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # draw two arrows (left and right) on the bottom of the screen

        blocks = [block for block in BlockType]
        block = Block(
            blocks[current_block_to_display], cell_size, current_color, rotation
        )
        block_rects = block.get_rect()

        # rotation button:
        rotation_button = Rect(100, 650, 100, 20)
        pygame.draw.rect(screen, "green", rotation_button)
        if rotation_button.collidepoint(mouse_pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                rotation += 1
                if rotation > 3:
                    rotation = 0

        block.draw_block(screen=screen, x=250, y=650)

        for rect in block_rects:

            rect.x = 250 + rect.x
            rect.y = 650 + rect.y

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(mouse_pos):

                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos

                    offset_x = rect.x - mouse_x
                    offset_y = rect.y - mouse_y

            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    rect.x = (mouse_x + offset_x) - (mouse_x + offset_x) % cell_size
                    rect.y = (mouse_y + offset_y) - (mouse_y + offset_y) % cell_size

                    last_block_x = rect.x
                    last_block_y = rect.y

                    block.draw_block(screen, last_block_x, last_block_y)

            elif event.type == pygame.MOUSEBUTTONUP:

                if rectangle_draging:
                    # change x and y to fit the grid
                    last_block_x = last_block_x - last_block_x % cell_size
                    last_block_y = last_block_y - last_block_y % cell_size

                    if board.add_block(
                        block, last_block_x, last_block_y, player=current_player
                    ):
                        current_player.has_moved = True
                        current_player_number += 1
                        if current_player_number > 3:
                            current_player_number = 0

                    rectangle_draging = False
                    pygame.event.post(pygame.event.Event(pygame.NOEVENT))



        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
