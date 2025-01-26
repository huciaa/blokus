# Example file showing a circle moving on screen
import pygame
from field import BlockType, Block
from board import Board
from game import players, switch_player
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
offset_y = 0
offset_x = 0

rotation = 0

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

board = Board(screen=screen)
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

        blocks = list(BlockType)
        block = Block(
            blocks[current_block_to_display], cell_size, current_color, rotation
        )
        block_rects = block.get_rect()
        block.draw_block(screen=screen, x=250, y=650)

        ## uses keyboard left right arrows
        current_block_to_display = UI.switch_current_block(
            event=event,
            current_block_to_display=current_block_to_display,
            nr_of_blocks=len(blocks),
        )

        # rotation button:
        rotation = UI.draw_rotation_button(screen, mouse_pos, event, rotation)

        for rect in block_rects:

            rect.x = 250 + rect.x
            rect.y = 650 + rect.y

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(mouse_pos):
                    rectangle_draging, offset_x, offset_y = UI.handle_click_on_block(
                        event, rect
                    )
            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    last_block_x, last_block_y = UI.handle_block_in_motion(
                        screen, event, rect, offset_x, offset_y, cell_size, block
                    )
            elif event.type == pygame.MOUSEBUTTONUP:

                if rectangle_draging:
                    if board.add_block(
                        block, last_block_x, last_block_y, player=current_player
                    ):

                        current_player_number = switch_player(
                            current_player, current_player_number
                        )

                    rectangle_draging = False
                    pygame.event.post(pygame.event.Event(pygame.NOEVENT))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
