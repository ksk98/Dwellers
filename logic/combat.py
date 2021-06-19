import jsonpickle

import context
from characters.hit import Hit
from characters.player import Player
from characters.character import Character
from characters.enemies.enemy_base import EnemyBase
from network.communication import communicate
from views.concrete.view_combat import ViewCombat
from views.view_enum import Views


class Combat:
    def __init__(self, players: list[Character], enemies: list[Character]):
        self._players = players
        self._enemies = enemies
        self._combat_view = ViewCombat(False)
        self._outcomes = list[str]()
        self._character_with_turn: Character = None
        self._is_host = context.GAME.lobby.local_lobby

        self._queue: list[Character] = self._players + self._enemies
        self._queue.sort(key=self._compareEnergy)

    def start(self):
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
        context.GAME.view_manager.set_current(Views.COMBAT)
        self._new_turn()  # set turn order for all characters
        self._character_with_turn = self._queue.pop(0)
        self._make_turn()
        context.GAME.view_manager.refresh()

    def receive_turn_data(self, hit: Hit):
        if self._is_host:
            self._broadcast_data()

        char_id = self._character_with_turn.id
        char = self.get_character_with_id(char_id)
        outcome = char.get_hit(hit.damage, hit.damage_type, hit.attacker, hit.attack, hit.energy_damage)
        if self._is_host:
            self._check_win()
        self._next_character_in_queue()
        context.GAME.view_manager.refresh()

    def _broadcast_data(self):
        for client in context.GAME.sockets.values():
            communicate(client, [])

    def _make_turn(self):
        if type(self._character_with_turn) == EnemyBase:
            if self._is_host:
                self._character_with_turn.act(self._get_alive_players())
            # else: wait for an update
        else:
            # Check if this is my turn
            if context.GAME.lobby.get_local_participant().player_id == self._character_with_turn.id:
                self._my_turn()
            # else: wait for an update

    def _my_turn(self):
        pass

    def _give_player_turn(self, player_id: int):
        if player_id == 0:
            self._my_turn()
        else:
            communicate()

    def _my_turn(self):
        pass

    def make_hit(self, hit: Hit):
        target = self.get_character_with_id(hit.target_id)
        if target is not None and target.id == self.get_current_character_id():
            # host broadcasts valid hit
            if context.GAME.lobby.local_lobby:
                pickled_hit = jsonpickle.encode(hit)
                for client in context.GAME.sockets.values():
                    communicate(client,
                                ["GAMEPLAY", "ACTION:ATTACK", "CONTENT-LENGTH:" + str(len(pickled_hit))],
                                pickled_hit)
            # take a hit
            outcome = target.get_hit(hit.damage, hit.damage_type, hit.attacker, hit.attack, hit.energy_damage)
            self.add_outcome(outcome)
            # TODO PRINT...

    def _check_win(self):
        if len(self._get_alive_enemies()) == 0:
            self._win()
        elif len(self._get_alive_players()) == 0:
            self._defeat()

    def end_combat(self, is_won: bool):
        if is_won:
            context.GAME.view_manager.set_current(Views.ROOM)
        # else: game.close

    def _next_character_in_queue(self):
        if len(self._queue) > 0:
            self._character_with_turn = self._queue.pop(0)
        else:
            self._new_turn()
            self._next_character_in_queue()

    def _new_turn(self):
        self._queue: list[Character] = self._players + self._enemies
        self._queue.sort(key=self._compareEnergy)

    def _get_alive_players(self) -> list[Character]:
        alive_players = list[Character]()
        for player in self._players:
            if player.hp > 0:
                alive_players.append(player)
        return alive_players

    def _get_alive_enemies(self) -> list[Character]:
        alive_enemies = list[Character]()
        for enemy in self._enemies:
            if enemy.hp > 0:
                alive_enemies.append(enemy)
        return alive_enemies

    def get_character_with_id(self, id: int):
        for char in self._players:
            if char.id == id:
                return char
        for char in self._enemies:
            if char.id == id:
                return char
        return None

    def get_current_character_id(self) -> int:
        return self._character_with_turn.id

    def add_outcome(self, outcome: str):
        pass

    @staticmethod
    def _win():
        for client in context.GAME.sockets.values():
            communicate(client, ["GAMEPLAY", "ACTION:WIN"])

    @staticmethod
    def _defeat():
        for client in context.GAME.sockets.values():
            communicate(client, ["GAMEPLAY", "ACTION:DEFEAT"])

    @staticmethod
    def _compareEnergy(c: Character):
        return c.base_energy
