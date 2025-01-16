import enum
from pygame.rect import Rect

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


class Block:

    def __init__(self, block_type: BlockType, block_size: int):
        self.block_type = block_type
        self.block_size = block_size

    

    def get_rect(self) -> list[Rect]:


        ## squares
        if self.block_type == BlockType.sqaure:
            return [ Rect(0, 0, self.block_size, self.block_size) ]
        elif self.block_type == BlockType.sqaure_2x2:
            return [ Rect(0, 0, self.block_size * 2, self.block_size * 2) ]
        
        ## rectangles
        elif self.block_type == BlockType.rectangle_2x1:
            return [ Rect(0, 0, self.block_size * 2, self.block_size) ] 
        elif self.block_type == BlockType.rectangle_3x1:
            return [ Rect(0, 0, self.block_size * 3, self.block_size) ]
        elif self.block_type == BlockType.rectangle_4x1:
            return [ Rect(0, 0, self.block_size * 4, self.block_size) ]
        elif self.block_type == BlockType.rectangle_5x1:
            return [ Rect(0, 0, self.block_size * 5, self.block_size) ]
        
        ## L shapes
        elif self.block_type == BlockType.L_4x2:
            vertical_shape = Rect(0, 0, self.block_size * 4, self.block_size)
            horizontal_shape = Rect(0, 0, self.block_size, self.block_size * 2)
            return [vertical_shape, horizontal_shape]
        
        elif self.block_type == BlockType.L_5x2:
            vertical_shape = Rect(0, 0, self.block_size * 5, self.block_size)   
            horizontal_shape = Rect(0, 0, self.block_size, self.block_size * 2)


            # concatenate the two shapes together
            return [ vertical_shape, horizontal_shape ]
