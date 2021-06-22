import jsonpickle

import context
from characters.character import Character
from characters.hit import Hit
from network.communication import communicate
from views.concrete.view_combat import ViewCombat
from views.concrete.view_defeat import ViewDefeat
from views.view_enum import Views


class Combat:
    def __init__(self, players: list[Character], enemies: list[Character]):
        self._end = False
        self._players = players
        self._enemies = enemies
        self._is_my_turn = False
        self._wait_for_update = False
        self._outcomes = list[str]()
        self._combat_view = ViewCombat(False, self._outcomes)
        self._is_host = context.GAME.lobby.local_lobby
        self._queue = list[Character]()

        self._next_character_in_queue()

    def start(self):
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
        context.GAME.view_manager.set_current(Views.COMBAT)
        self.battle()

    def battle(self):
        # TODO BUG: energy not updating on client
        while True:
            if self._wait_for_update or self._is_my_turn or self._end:
                context.GAME.view_manager.refresh()
                break
            self._make_turn()
            if self._wait_for_update or self._is_my_turn or self._end:
                context.GAME.view_manager.refresh()
                break
            else:
                context.GAME.view_manager.refresh()

    def _make_turn(self):
        if self._character_with_turn in self._enemies:
            if self._is_host:
                if len(self.get_alive_players()) > 0:
                    self.add_outcome(self._character_with_turn.act(self.get_alive_players()))
                self._check_win()
                self._next_character_in_queue()
            else:
                self._wait_for_update = True
        else:
            # Check if this is my turn
            if context.GAME.lobby.get_local_participant().player_id == self._character_with_turn.id:
                self._my_turn()
                self._check_win()
            else:
                self._wait_for_update = True

    def _my_turn(self):
        if not self._is_my_turn:
            self._combat_view = ViewCombat(True, self._outcomes)
            context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
            context.GAME.view_manager.set_current(Views.COMBAT)
            self._is_my_turn = True

    def make_hit(self, hit: Hit):
        target = self.get_character_with_id(hit.target_id)
        if target is not None:
            if self._character_with_turn.id == hit.user_id:
                # take a hit
                outcome = target.get_hit(hit.damage, hit.damage_type, hit.attacker, hit.attack, hit.energy_damage)
                self.add_outcome(outcome)

                self._check_win()
                # host broadcasts valid hit
                if context.GAME.lobby.local_lobby and self._end:
                    pickled_hit = jsonpickle.encode(hit)
                    for client in context.GAME.sockets.values():
                        communicate(client,
                                    ["GAMEPLAY", "ACTION:ATTACK", "CONTENT-LENGTH:" + str(len(pickled_hit))],
                                    pickled_hit)
                self._wait_for_update = False
                context.GAME.view_manager.refresh()
                self._next_character_in_queue()
                self.battle()

    def get_outcomes(self) -> list[str]:
        return self._outcomes

    def _check_win(self):
        if context.GAME.lobby.local_lobby:
            if len(self.get_alive_enemies()) == 0:
                self._communicate_win()
                self.win()
            elif len(self.get_alive_players()) == 0:
                self._communicate_defeat()
                self.defeat()

    def _next_character_in_queue(self):
        if len(self._queue) > 0:
            self._character_with_turn = self._queue.pop(0)
            self._check_alive()
        else:
            self._new_turn()
            self._next_character_in_queue()

    def _new_turn(self):
        self._queue: list[Character] = self.get_alive_players() + self.get_alive_enemies()
        self._queue.sort(key=self._compareEnergy)

    def get_alive_players(self) -> list[Character]:
        alive_players = list[Character]()
        for player in self._players:
            if player.hp > 0:
                alive_players.append(player)
        return alive_players

    def get_alive_enemies(self) -> list[Character]:
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

    def rest_current_character(self):
        self.add_outcome(self._character_with_turn.rest(False))
        self._next_character_in_queue()
        self._check_win()
        self._wait_for_update = False
        self.battle()

    def current_character_missed(self, miss_text: str):
        self.add_outcome(miss_text)
        self._next_character_in_queue()
        self._wait_for_update = False
        self.battle()

    def add_outcome(self, outcome: str):
        self._outcomes.append(outcome)
        pass

    def end_turn(self):
        self._is_my_turn = False
        self._combat_view = ViewCombat(False, self._outcomes)
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
        context.GAME.view_manager.refresh()
        self._check_win()
        self._next_character_in_queue()
        self.battle()

    def get_current_character_name(self) -> str:
        return self._character_with_turn.name

    def win(self):
        self._end = True
        self._enemies.clear()
        for player in self._players:
            player.energy = player.base_energy
        context.GAME.view_manager.remove_view_for_enum(Views.COMBAT)
        context.GAME.combat = None
        context.GAME.view_manager.set_current(Views.ROOM)

    def defeat(self):
        self._end = True
        context.GAME.abandon_lobby()
        context.GAME.view_manager.remove_view_for_enum(Views.COMBAT)
        context.GAME.combat = None
        context.GAME.view_manager.set_new_view_for_enum(Views.DEFEAT, ViewDefeat())
        context.GAME.view_manager.set_current(Views.DEFEAT)

    def _check_alive(self):
        if self._character_with_turn.hp <= 0:
            self._next_character_in_queue()

    @staticmethod
    def _communicate_win():
        for client in context.GAME.sockets.values():
            communicate(client, ["GAMEPLAY", "ACTION:WIN"])

    @staticmethod
    def _communicate_defeat():
        for client in context.GAME.sockets.values():
            communicate(client, ["GAMEPLAY", "ACTION:DEFEAT"])

    @staticmethod
    def _compareEnergy(c: Character):
        return c.base_energy
