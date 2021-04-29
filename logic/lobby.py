class Lobby:
    def __init__(self):
        self.external_lobby = False
        self.participants = []
        self.host_id = -2

    def add_participant(self, participant):
        self.participants.append(participant)

    def remove_participant(self, participant):
        self.participants.remove(participant)

    def get_host(self):
        for participant in self.participants:
            if participant.id == self.host_id:
                return participant

        return None
