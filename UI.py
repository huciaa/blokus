from game import Player
from pygame import Surface, Rect
from pygame.event import Event
from field import Block
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
            f"{player.player_type.value}: {player.points} ",
            False,
            player.player_type.value,
            "GREY",
        )
        screen.blit(text_surface, (620, offset))
        offset += 100


def draw_rotation_button(
    screen: Surface,
    mouse_pos: tuple[int, int],
    current_event: Event,
    current_rotation: int,
) -> int:

    rotation_button = Rect(100, 650, 100, 20)
    pygame.draw.rect(screen, "green", rotation_button)
    if rotation_button.collidepoint(mouse_pos):
        if current_event.type == pygame.MOUSEBUTTONDOWN:
            current_rotation += 1
            if current_rotation > 3:
                current_rotation = 0

    return current_rotation


def switch_current_block(
    event: Event, current_block_to_display: int, nr_of_blocks: int
) -> int:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            current_block_to_display -= 1
            if current_block_to_display < 0:
                current_block_to_display = nr_of_blocks - 1

        if event.key == pygame.K_RIGHT:
            current_block_to_display += 1
            if current_block_to_display >= nr_of_blocks:
                current_block_to_display = 0

    return current_block_to_display


def handle_click_on_block(event: Event, rect: Rect):
    rectangle_draging = True
    mouse_x, mouse_y = event.pos

    offset_x = rect.x - mouse_x
    offset_y = rect.y - mouse_y

    return rectangle_draging, offset_x, offset_y
    


def handle_block_in_motion(
    screen: Surface,
    event: Event,
    rect: Rect,
    offset_x: int,
    offset_y: int,
    cell_size: int,
    block: Block,
) -> tuple[int, int]:
    
    mouse_x, mouse_y = event.pos
    rect.x = (mouse_x + offset_x) - (mouse_x + offset_x) % cell_size
    rect.y = (mouse_y + offset_y) - (mouse_y + offset_y) % cell_size

    last_block_x = rect.x - rect.x % cell_size
    last_block_y = rect.y - rect.y % cell_size

    block.draw_block(screen, last_block_x, last_block_y)

    return last_block_x, last_block_y
