from enum import Enum


class PlayerType(Enum):
    BLUE = "BLUE"
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"

    def color(self):
        return self.value


class Player:

    def __init__(self, player_type: PlayerType):
        self.player_type = player_type
        self.points = 0
        self.has_moved = False

    def increase_points(self, points):
        self.points = self.points + points


players: list[Player] = [
    Player(PlayerType.BLUE),
    Player(PlayerType.RED),
    Player(PlayerType.GREEN),
    Player(PlayerType.YELLOW),
]


def switch_player(current_player: Player, current_player_number: int):

    current_player.has_moved = True
    current_player_number += 1
    if current_player_number > 3:
        current_player_number = 0

    return current_player_number
