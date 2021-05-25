from settings import settings


class Participant:
    def __init__(self, player_id: int):
        self.character = None
        self.player_id = player_id
        self.name = settings["PLAYER_NAME"]
