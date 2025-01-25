from game import Player
from field import Block, BlockType
from board import Board
from pygame import Surface, Rect
from pygame.event import Event
import pygame



def draw_score_board(screen: Surface, players: list[Player]):

    my_font = pygame.font.SysFont("Comic Sans MS", 30)
    text_surface = my_font.render("Leaderboard:", False, (0, 0, 0))
    screen.blit(text_surface, (620, 0))

    players_ordered: list[Player] = None

    for player in players:
        if players_ordered is None:
            players_ordered = [player]
        else:
            for index, ordered_player in enumerate(players_ordered):

                if player.points > ordered_player.points:
                    player_index = index
                else:
                    player_index = len(players_ordered)

            players_ordered = (
                players_ordered[0:player_index]
                + [player]
                + players_ordered[player_index:]
            )

    offset = 100
    for player in players_ordered:
        text_surface = my_font.render(
            f"player {player.player_type.value}: {player.points} ", False, (0, 0, 0)
        )
        screen.blit(text_surface, (620, offset))
        offset += 100


def draw_rotation_button(
    screen: Surface,
    mouse_pos: tuple[int, int],
    event: Event,
    current_rotation: int,
) -> int:

    rotation_button = Rect(100, 650, 100, 20)
    pygame.draw.rect(screen, "green", rotation_button)
    if rotation_button.collidepoint(mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_rotation += 1
            if current_rotation > 3:
                current_rotation = 0

    return current_rotation

def draw_current_block(
    screen: Surface,
    mouse_pos: tuple[int, int],
    event: Event,
    rotation: int,
    color,
    board: Board,
    current_player: Player,
    current_block_to_display: int,
    cell_size,
    rectangle_draging = False
    
):
    
        blocks = [block for block in BlockType]
        block = Block(
            blocks[current_block_to_display], cell_size, color, rotation
        )
        block_rects = block.get_rect()

        block.draw_block(screen=screen, x=250, y=650)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block_to_display -= 1
                if current_block_to_display < 0:
                    current_block_to_display = len(blocks) - 1

            if event.key == pygame.K_RIGHT:
                current_block_to_display += 1
                if current_block_to_display >= len(blocks):
                    current_block_to_display = 0

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
