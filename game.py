from enum import Enum


class PlayerType(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"


    def color(self):
        return self.value

class Player:

    def __init__(self, player_type: PlayerType):
        self.player_type = player_type
        self.points = 0
        self.has_moved = False


