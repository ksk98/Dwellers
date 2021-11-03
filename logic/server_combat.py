import jsonpickle

import context
import logic.client_combat
from characters.character import Character
from characters.hit import Hit
from network import communication, utility


class ServerCombat:
    """
    Controls whole combat - sets the turn order, all outcomes and values, decides if the battle is won or lost.
    Clients using ClientCombat are sending all info about what they want to do and this class
    is deciding if they can do this. If they can, the outcome is sent to all players,
    if not the appropriate message is sent to the client.
    """
    def __init__(self):
        # Character currently having a turn
        self._character_with_turn: Character = None

        # Turn order
        self._queue: list[Character]()

        # List of enemies
        self._enemies = context.GAME.current_room.get_enemies()

        # List of players
        self._players = context.GAME.get_players()

    # public methods

    def act(self):
        """
        Acts as enemy character
        """
        while True:
            if self._character_with_turn in self._enemies:
                if self._check_win():
                    return
                players = self._get_alive_players()
                outcome, hit = self._character_with_turn.act(players)
                self._get_next_character()
                self.send_outcome(outcome, hit, self._character_with_turn.id)
            else:
                break

    def attack(self, user_id: int, target_id: int, type: str) -> tuple[str, Hit, int]:
        """
        Execute received attack
        :param user_id: attacker's id
        :param target_id: target's id
        :param type: attack's type
        :return: tuple - outcome string, hit object and id of next character in queue
        """
        user = context.GAME.combat.get_character_with_id(user_id)
        if user is None:
            self._get_next_character()
            return "Attacker's object not found! Skipping turn...", \
                   None, \
                   self._character_with_turn.id

        if user.id != self._character_with_turn.id:
            self._get_next_character()
            return "Attacker's id mismatch with server! Skipping turn...", \
                   None, \
                   self._character_with_turn.id

        target = context.GAME.combat.get_character_with_id(target_id)
        if target is None:
            self._get_next_character()
            return "Target's object not found! Skipping turn...", \
                   None, \
                   self._character_with_turn.id

        attack = user.get_attack(type)
        if attack is not None:
            outcome, hit = user.use_skill_on(attack, target)
            if outcome == "":  # not enough energy
                return outcome, hit, self._character_with_turn.id

            self._get_next_character()
            return outcome, hit, self._character_with_turn.id

    def check_if_player_exists(self):
        """
        Checks if character with turn is still in the game
        """
        # Combat hasn't started yet so skip
        if context.GAME.combat is None:
            return

        # Search for it...
        exists = False
        current_id = self._character_with_turn.id
        # ... among players
        for char in context.GAME.get_players():
            if char.id == current_id:
                exists = True
                break
        # ... and enemies
        for char in self._enemies:
            if char.id == current_id or exists:  # because if player was found there's no need to search among enemies
                exists = True
                break

        if not exists:
            self._players = context.GAME.get_players()
            self._get_next_character()

    def remove_player_from_queue(self, player_id: int):
        for character in self._queue:
            if character.id == player_id:
                self._queue.remove(character)

    def rest(self, user_id: int):
        """
        Execute rest action
        :param user_id: user that is trying to rest
        :return: tuple - string with outcome, none and next character's id
        """
        character = context.GAME.combat.get_character_with_id(user_id)
        if character is None:
            self._get_next_character()
            return "Character not found! Skipping turn...", None, self._character_with_turn.id

        if character.id != self._character_with_turn.id:
            self._get_next_character()
            return "Attacker's id mismatch with server! Skipping turn...", None, self._character_with_turn.id

        outcome, hit = character.rest()
        self._get_next_character()
        return outcome, hit, self._character_with_turn.id

    def send_outcome(self, outcome: str, hit: Hit, next_id: int, sckt=None):
        """
        Sends all that has happened during turn to clients
        :param outcome: string describing what happened
        :param hit: object containing all values that has been modified
        :param next_id: character's id that has next turn
        :param sckt: client socket (for replying that he has no enough energy)
        """
        # Not enough energy
        if outcome == "":
            if sckt is None:
                context.GAME.combat.handle_outcome(next_id)
            else:
                communication.communicate(sckt, ["COMBAT", "ACTION:NO_ENERGY"])
            return

        if self._check_win():
            return
        all_outcomes = [outcome, hit, next_id]
        pickled_outcomes = jsonpickle.encode(all_outcomes)

        for client in context.GAME.sockets.values():
            answer = communication.communicate_and_get_answer(client,
                                                              ["COMBAT",
                                                               "ACTION:OUTCOME",
                                                               "TURN:" + str(id),
                                                               "CONTENT-LENGTH:" + str(len(pickled_outcomes))],
                                                              pickled_outcomes)

            action = utility.get_value_of_argument(answer, "ACTION")
            status = utility.get_value_of_argument(answer, "STATUS")
            if action != "OUTCOME_RECEIVE" or status != "OK":
                return utility.get_ip_and_address_of_client_socket(sckt) + ": " + status

        context.GAME.combat.handle_outcome(next_id, outcome, hit)
        self.act()

    def start(self):
        """
        Starts combat and sends info about it to clients
        :return:
        """
        self._new_queue()
        id = self._character_with_turn.id
        if context.GAME.lobby.local_lobby:
            # Check answer for all clients and then continue...
            for client in context.GAME.sockets.values():
                answer = communication.communicate_and_get_answer(client,
                                                                  ["COMBAT",
                                                                   "ACTION:START",
                                                                   "TURN:" + str(id)])
                action = utility.get_value_of_argument(answer, "ACTION")
                status = utility.get_value_of_argument(answer, "STATUS")
                if action != "START" or status != "OK":
                    context.GAME.abandon_lobby()
        else:
            # ONLY HOST CAN USE THIS
            return

        context.GAME.combat = logic.client_combat.ClientCombat(id)
        context.GAME.combat.start()
        self.act()

    # private

    def _communicate_end(self, result: str):
        """
        Communicate that combat has ended
        :param result: "WIN" / "DEFEAT"
        :return: log
        """
        for client in context.GAME.sockets.values():
            answer = communication.communicate_and_get_answer(client,
                                                              ["COMBAT",
                                                               "ACTION:" + result])

            action = utility.get_value_of_argument(answer, "ACTION")
            status = utility.get_value_of_argument(answer, "STATUS")
            if action != "END_RECEIVE" or status != "OK":
                return utility.get_ip_and_address_of_client_socket(client) + ": " + status

    def _check_win(self):
        """
        Checks if combat can continue
        """
        if context.GAME.lobby.local_lobby:
            if len(self._get_alive_enemies()) == 0:
                self._communicate_end("WIN")
                context.GAME.combat.restore_energy()
                logic.client_combat.end_battle(True)
                return True
            elif len(self._get_alive_players()) == 0:
                self._communicate_end("DEFEAT")
                logic.client_combat.end_battle(False)
                return True
        return False

    def _check_alive(self):
        """
        Checks if current character with turn is alive...
        """
        if self._character_with_turn.hp <= 0:
            self._get_next_character()

    def _new_queue(self):
        """
        Creates new queue
        :return:
        """
        self._queue = self._get_alive_enemies() + self._get_alive_players()
        self._queue.sort(key=self._compare_energy, reverse=True)
        self._get_next_character()

    # getters

    def _get_alive_enemies(self) -> list[Character]:
        alive_enemies = list[Character]()
        for enemy in self._enemies:
            if enemy.hp > 0:
                alive_enemies.append(enemy)
        return alive_enemies

    def _get_alive_players(self) -> list[Character]:
        alive_players = list[Character]()
        for player in self._players:
            if player.hp > 0:
                alive_players.append(player)
        return alive_players

    def _get_next_character(self):
        """
        Gets next character from queue
        """
        if len(self._queue) > 0:
            self._character_with_turn = self._queue.pop(0)
            self._check_alive()            # character could have been killed
            self.check_if_player_exists()  # or leave
        else:
            self._new_queue()

    # static methods

    @staticmethod
    def _compare_energy(c: Character):
        """
        Comparator for queue sorting
        :param c: character
        :return: character's max energy
        """
        return c.get_base_energy()
