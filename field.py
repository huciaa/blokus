import enum
from pygame.rect import Rect
from pygame.sprite import Sprite
import pygame

class BlockType(enum.Enum):
    sqaure = "SQUARE"
    sqaure_2x2 = "SQUARE_2X2"

    rectangle_2x1 = "RECTANGLE_2X1"
    rectangle_3x1 = "RECTANGLE_3X1"
    rectangle_4x1 = "RECTANGLE_4X1"
    rectangle_5x1 = "RECTANGLE_5X1"

    L_4x2 = "L_4X2"
    L_5x2 = "L_5X2"


class Field:
    def __init__(self, pos_x, pos_y, width: int, height: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

        self.border = Rect(pos_x, pos_y, width, height)
        self.inner = Rect(pos_x + 2, pos_y + 2, width - 4, height - 4)

        self.field_index_x = pos_x // width
        self.field_index_y = pos_y // height

        self.used = 0

    def __str__(self):
    
        return f"Field: {self.field_index_x} {self.field_index_y} {self.used}"

    def __repr__(self):
    
        return f"Field: {self.field_index_x} {self.field_index_y} {self.used}"

class Block:

    def __init__(self, block_type: BlockType, block_size: int, color: str, rotation: int = 0):
        self.block_type = block_type
        self.block_size = block_size
        self.rotation = rotation

        self.used_fields = []

        self.color = color

    def __str__(self):
        
        return f"Block: {self.block_type} {self.block_size} {self.rotation}"

    def draw_block(self, screen, x, y):
        block_rects = self.get_rect()
        for rect in block_rects:
            rect.x = x + rect.x
            rect.y = y + rect.y
            pygame.draw.rect(screen, self.color, rect)


    def get_rect(self) -> list[Rect]:

        ## squares
        if self.block_type == BlockType.sqaure:
            return [Rect(0, 0, self.block_size, self.block_size)]
        elif self.block_type == BlockType.sqaure_2x2:
            return [Rect(0, 0, self.block_size * 2, self.block_size * 2)]

        ## rectangles
        elif self.block_type == BlockType.rectangle_2x1 and self.rotation in [0, 2]:
            return [Rect(0, 0, self.block_size * 2, self.block_size)]
        elif self.block_type == BlockType.rectangle_2x1 and self.rotation in [1, 3]:
            return [Rect(0, 0, self.block_size, self.block_size * 2)]
        elif self.block_type == BlockType.rectangle_3x1 and self.rotation in [0, 2]:
            return [Rect(0, 0, self.block_size * 3, self.block_size)]
        elif self.block_type == BlockType.rectangle_3x1 and self.rotation in [1, 3]:
            return [Rect(0, 0, self.block_size, self.block_size * 3)]
        elif self.block_type == BlockType.rectangle_4x1 and self.rotation in [0, 2]:
            return [Rect(0, 0, self.block_size * 4, self.block_size)]
        elif self.block_type == BlockType.rectangle_4x1 and self.rotation in [1, 3]:
            return [Rect(0, 0, self.block_size, self.block_size * 4)]
        elif self.block_type == BlockType.rectangle_5x1 and self.rotation in [0, 2]:
            return [Rect(0, 0, self.block_size * 5, self.block_size)]
        elif self.block_type == BlockType.rectangle_5x1 and self.rotation in [1, 3]:
            return [Rect(0, 0, self.block_size, self.block_size * 5)]

        ## L shapes
        elif self.block_type == BlockType.L_4x2:
            if self.rotation == 0:
                return [
                    Rect(0, 0, self.block_size * 4, self.block_size),
                    Rect(0, 0, self.block_size, self.block_size * 2),
                ]
            elif self.rotation == 1:
                return [
                    Rect(self.block_size * 1, 0, self.block_size, self.block_size * 4),
                    Rect(0, 0, self.block_size * 2, self.block_size),
                ]
            elif self.rotation == 2:
                return [
                    Rect(0, self.block_size * 1, self.block_size * 4, self.block_size),
                    Rect(self.block_size * 3, 0, self.block_size, self.block_size * 2),
                ]
            elif self.rotation == 3:
                return [
                    Rect(0, 0, self.block_size, self.block_size * 4),
                    Rect(0, self.block_size * 3, self.block_size * 2, self.block_size),
                ]

        elif self.block_type == BlockType.L_5x2:
            if self.rotation == 0:
                return [
                    Rect(0, 0, self.block_size * 5, self.block_size),
                    Rect(0, 0, self.block_size, self.block_size * 2),
                ]
            elif self.rotation == 1:
                return [
                    Rect(self.block_size * 1, 0, self.block_size, self.block_size * 5),
                    Rect(0, 0, self.block_size * 2, self.block_size),
                ]
            elif self.rotation == 2:
                return [
                    Rect(0, self.block_size * 1, self.block_size * 5, self.block_size),
                    Rect(self.block_size * 4, 0, self.block_size, self.block_size * 2),
                ]
            elif self.rotation == 3:
                return [
                    Rect(0, 0, self.block_size, self.block_size * 5),
                    Rect(0, self.block_size * 4, self.block_size * 2, self.block_size),
                ]

    def get_sprite(self) -> Sprite:
        pass

    def rotate(self):

        pass
