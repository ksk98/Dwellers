from config import config
from logic.participant import Participant


class Lobby:
    def __init__(self, password: str = ""):
        self.external_lobby = False
        self.participants: list[Participant] = []
        self.__password = password
        self.address = ""
        self.port = 0

    def add_participant(self, participant) -> bool:
        if self.is_full():
            return False

        self.participants.append(participant)
        return True

    def remove_participant(self, id) -> bool:
        if len(self.participants) == 0:
            return False

        participant = self.get_participant_of_id(id)
        if participant is None:
            return False

        self.participants.remove(participant)
        return True

    def get_host(self) -> Participant:
        for participant in self.participants:
            if participant.player_id == 0:
                return participant

        return None

    def has_participant_of_id(self, pid: int) -> bool:
        for part in self.participants:
            if part.player_id == pid:
                return True

        return False

    def get_participant_of_id(self, pid: int) -> Participant:
        for part in self.participants:
            if part.player_id == pid:
                return part

        return None

    def is_empty(self) -> bool:
        return len(self.participants) == 0

    def is_full(self) -> bool:
        if len(self.participants) == config["MAX_PLAYERS"]:
            return True

        return False

    def has_password(self) -> bool:
        return not self.__password == ""

    def try_password(self, password: str) -> bool:
        return self.__password == password
