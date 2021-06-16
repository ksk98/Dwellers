from config import config
from logic.participant import Participant


class Lobby:
    """
    Class representing a lobby. Contains no network internals, only the ones that matter gameplay-wise.
    """
    def __init__(self, password: str = ""):
        self.external_lobby = False
        self.participants: list[Participant] = []
        self.local_player_id = -1
        self.__password = password

    def add_participant(self, participant) -> bool:
        """
        Add a player object to the lobby.
        :return True on success
        """
        if self.is_full():
            return False

        self.participants.append(participant)
        return True

    def remove_participant(self, player_id) -> bool:
        """
        Remove player object from lobby.
        :return True on success
        """
        if len(self.participants) == 0:
            return False

        participant = self.get_participant_of_id(player_id)
        if participant is None:
            return False

        self.participants.remove(participant)
        return True

    def get_host(self) -> Participant:
        """
        Get player object of host. If for some god-knows-what reason there is none, returns None.
        """
        for participant in self.participants:
            if participant.player_id == 0:
                return participant

        return None

    def has_participant_of_id(self, pid: int) -> bool:
        """
        Check if lobby has a player of given ID.
        """
        for part in self.participants:
            if part.player_id == pid:
                return True

        return False

    def get_participant_of_id(self, pid: int) -> Participant:
        """
        Get player object of given ID. Returns None if none exists.
        """
        for part in self.participants:
            if part.player_id == pid:
                return part

        return None

    def get_local_participant(self):
        return self.get_participant_of_id(self.local_player_id)

    def is_empty(self) -> bool:
        """
        Check if lobby is empty.
        """
        return len(self.participants) == 0

    def is_full(self) -> bool:
        """
        Check if lobby is full.
        """
        if len(self.participants) == config["MAX_PLAYERS"]:
            return True

        return False

    def has_password(self) -> bool:
        """
        Check if lobby is password protected.
        """
        return not self.__password == ""

    def try_password(self, password: str) -> bool:
        """
        Check if a given password is valid for lobby.
        """
        return self.__password == password
