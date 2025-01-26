from field import Block, Field
from pygame.surface import Surface
from game import Player, PlayerType
import pygame


class IllegalMove(Exception):
    pass


class BlockOnBoard:
    block: Block
    x: int
    y: int

    def __init__(self, block: Block, x: int, y: int):
        self.block = block
        self.x = x
        self.y = y


class Board:
    blocks: list[BlockOnBoard]

    fields: list[Field]
    used_fields: list[tuple[Field, Player]]

    def __init__(self, screen: Surface, cell_size: int = 30):
        self.blocks = []
        self.fields = []
        self.used_fields = []
        number_of_cells_in_line = 20
        self.screen = screen

        for x in range(number_of_cells_in_line):
            for y in range(number_of_cells_in_line):
                field = Field(x * cell_size, y * cell_size, cell_size, cell_size)
                self.fields.append(field)

        return

    def draw_board(
        self,
    ):

        for field in self.fields:
            pygame.draw.rect(self.screen, "black", field.border)
            pygame.draw.rect(self.screen, "white", field.inner)

            ## corner fields has colors
            if field.field_index_x == 0 and field.field_index_y == 0:
                pygame.draw.rect(self.screen, "red", field.inner)
            elif field.field_index_x == 0 and field.field_index_y == 19:
                pygame.draw.rect(self.screen, "blue", field.inner)
            elif field.field_index_x == 19 and field.field_index_y == 0:
                pygame.draw.rect(self.screen, "green", field.inner)
            elif field.field_index_x == 19 and field.field_index_y == 19:
                pygame.draw.rect(self.screen, "yellow", field.inner)

        for block_on_board in self.blocks:
            block = block_on_board.block
            x = block_on_board.x
            y = block_on_board.y
            block.draw_block(self.screen, x, y)

    def check_if_field_is_used(self, x: int, y: int):
        for field in self.fields:
            if field.field_index_x == x and field.field_index_y == y:
                return field.used

    def get_fields_to_use(self, block: Block, x: int, y: int) -> list[Field]:
        
        field_to_use_coordinates: list[tuple[int,int]] = []
        fields_to_use: list[Field] = []

        # block use this fields
        for rect in block.get_rect():

            # Check which cells block uses

            left_border = (x + rect.x) // 30
            right_border = (x + rect.x + (rect.right - rect.left)) // 30

            top_border = (y + rect.y) // 30
            bottom_border = (y + rect.y + (rect.bottom - rect.top)) // 30

            print(left_border, right_border, top_border, bottom_border)

            if (
                left_border < 0
                or right_border > 20
                or top_border < 0
                or bottom_border > 20
            ):
                print(
                    f"Block is out of board: {left_border} {right_border} {top_border} {bottom_border}"
                )
                raise IllegalMove(
                    f"Block is out of board: {left_border} {right_border} {top_border} {bottom_border}"
                )

            for used_x in range(left_border, right_border):
                for used_y in range(top_border, bottom_border):
                    field_to_use_coordinates.append((used_x, used_y))

        for x, y in set(field_to_use_coordinates):
            for field in self.fields:
                if field.field_index_x == x and field.field_index_y == y:
                    fields_to_use.append(field)

        return fields_to_use

    def add_block(self, block: Block, x: int, y: int, player: Player):

        try:
            fields_to_use = self.get_fields_to_use(block, x, y)

        except IllegalMove:
            return False

        if player.has_moved is False:
            if not self.validate_first_move(block, fields_to_use):
                return False
        else:
            if not self.validate_next_move(fields_to_use, player):
                return False

        for field in fields_to_use:
            if field.used:
                return False

        for field in fields_to_use:
            field.used = 1
            self.used_fields.append((field, player))

        self.blocks.append(BlockOnBoard(block, x, y))
        player.increase_points(len(fields_to_use))
        self.draw_board()
        return True

    def validate_first_move(self, block: Block, fields_to_use: list[Field]):

        if block.color == PlayerType.RED.value:
            for field in fields_to_use:
                if field.field_index_x == 0 and field.field_index_y == 0:
                    return True
        elif block.color == PlayerType.BLUE.value:
            for field in fields_to_use:
                if field.field_index_x == 0 and field.field_index_y == 19:
                    return True
        elif block.color == PlayerType.GREEN.value:
            for field in fields_to_use:
                if field.field_index_x == 19 and field.field_index_y == 0:
                    return True
        elif block.color == PlayerType.YELLOW.value:
            for field in fields_to_use:
                if field.field_index_x == 19 and field.field_index_y == 19:
                    return True
        else:
            return False

    def validate_next_move(
        self, fields_to_use: list[Field], current_player: Player
    ):

        player_fields = [field for field, player in self.used_fields if player == current_player]


        ## blocks should not touch existing player blocks , only corners are allowed
        for field in fields_to_use:
            for player_field in player_fields:
                if (
                    (abs(field.field_index_x - player_field.field_index_x) == 1 and abs(field.field_index_y - player_field.field_index_y) == 0) or
                    (abs(field.field_index_x - player_field.field_index_x) == 0 and abs(field.field_index_y - player_field.field_index_y) == 1)
                ):
                    print("Block is touching existing block - ", field )
                    return False
                
        ## a corner of the block should touch a corner of an existing player block
        for field in fields_to_use:
            for player_field in player_fields:
                if (
                    abs(field.field_index_x - player_field.field_index_x) == 1
                    and abs(field.field_index_y - player_field.field_index_y) == 1
                ):
                    print("Block is touching corner of existing block - ", field )
                    return True

