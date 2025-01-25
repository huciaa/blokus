# Example file showing a circle moving on screen
import pygame
from pygame import Rect
from field import BlockType, Block
from board import Board
from game import PlayerType, Player
import UI

# pygame setup
pygame.init()

screen_width = 880
screen_height = 820
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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    board.draw_board()
    UI.draw_score_board(screen, players)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # rotation button:
        rotation = UI.draw_rotation_button(screen, mouse_pos, event, rotation)

        # block
        UI.draw_current_block(
            screen,
            mouse_pos,
            event,
            rotation,
            current_color,
            board,
            current_player,
            current_block_to_display,
            cell_size,
        )

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
