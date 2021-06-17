from characters.player import Player
from settings import settings


class Participant:
    """
    Class representing a player.
    """
    def __init__(self, player_id: int):
        self.character = Player(settings["SELECTED_CHARACTER"])
        self.player_id = player_id
        self.name = settings["PLAYER_NAME"]
        self.ready = False
