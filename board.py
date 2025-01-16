from field import BlockType, Block


class BlockOnBoard:
    block: BlockType
    x: int
    y: int

    def __init__(self, block: Block, x: int, y: int):
        self.block = block
        self.x = x
        self.y = y



class Board:
    blocks: list[BlockOnBoard]

    def __init__(self):
        self.blocks = []
        return

    def add_block(self, block: Block, x: int, y: int):
        self.blocks.append(BlockOnBoard(block, x, y))
