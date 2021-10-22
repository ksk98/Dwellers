import context
import views.concrete.view_combat
from characters.character import Character
from characters.hit import Hit
from network import communication
from views.concrete.view_defeat import ViewDefeat
from views.concrete.view_room import ViewRoom
from views.view_enum import Views


class ClientCombat:
    def __init__(self, id_with_turn: int):
        # Id of player currently having turn
        self._id_with_turn = id_with_turn

        # List of all players in combat
        self._players = context.GAME.get_players()

        # List of all enemies
        self._enemies = context.GAME.current_room.get_enemies()

        # List of outcomes - strings containing info about previous turns
        self._outcomes = list[str]()

        # View object - displays all combat related stuff to user
        self._combat_view = None

        # This is my time to shine!
        self._is_my_turn = False

        # Local character
        self._local_participant = context.GAME.lobby.get_local_participant()

        # Local player id
        self._my_id = self._local_participant.player_id

        # Host socket
        self._host = context.GAME.host_socket

    def attack(self):
        """
        Execute attack action. Takes all necessary values and sends them to host or executes it.
        """
        # Take input
        target_index = self._combat_view.inputs.get("TARGET")[0]
        attack: str = self._combat_view.get_input_of_option("ATTACK TYPE")
        if attack == "Heal":
            targets = self.get_alive_players()
        else:
            targets = self.get_alive_enemies()

        target_id = targets[target_index].id

        # Send to host
        if not context.GAME.lobby.local_lobby:
            communication.communicate(self._host,
                                      ["COMBAT",
                                       "ACTION:ATTACK",
                                       "USER:" + str(self._my_id),
                                       "TARGET:" + str(target_id),
                                       "TYPE:" + attack])
        # Or execute as host
        else:
            outcome, hit, next_id = context.GAME.server_combat.attack(self._my_id, target_id, attack)
            context.GAME.server_combat.send_outcome(outcome, hit, next_id)

    def handle_outcome(self, new_turn: int = -1, outcome: str = "", hit: Hit = None):
        """
        Controls the CombatView object based on given parameters
        :param new_turn: id of character that has next turn
        :param outcome: string containing result of the turn
        :param hit: object containing all values modified during turn
        """
        if outcome == "" and hit is None:
            self._combat_view.not_enough_energy()

        else:
            self._outcomes.append(outcome)

            # As a host - don't deal damage 2nd time
            if hit is not None and not context.GAME.lobby.local_lobby:
                user = self.get_character_with_id(hit.user_id)
                target = self.get_character_with_id(hit.target_id)

                # Target
                target.deal_damage(hit.damage)
                target.deal_energy_damage(hit.energy_damage)

                # User
                user.deal_damage(hit.user_damage)
                user.take_energy(hit.energy_cost)

            self._create_new_view(new_turn)

    def rest(self):
        """
        Send rest action or executes it
        """
        if not context.GAME.lobby.local_lobby:
            communication.communicate(self._host,
                                      ["COMBAT",
                                       "ACTION:REST",
                                       "USER:" + str(self._my_id)])
        else:
            outcome, hit, next_id = context.GAME.server_combat.rest(self._my_id)
            context.GAME.server_combat.send_outcome(outcome, hit, next_id)

    def set_target_list_for_attack(self):
        """
        Sets the targets in CombatView based on selected attack type (heal - players and enemies otherwise)
        """
        attack: str = self._combat_view.get_input_of_next_option("ATTACK TYPE")
        if attack is None:
            return

        if attack == "Heal":
            prepared_targets = self._prepare_strings_for_targets(self.get_alive_players())
            self._combat_view.set_targets(prepared_targets)
        else:
            prepared_targets = self._prepare_strings_for_targets(self.get_alive_enemies())
            self._combat_view.set_targets(prepared_targets)

    def start(self):
        """
        Starts the combat - sets the view
        """
        self._create_new_view(self._id_with_turn)

    # Getters

    def get_alive_enemies(self) -> list[Character]:
        """
        Return all enemies with hp > 0
        :return: list of alive enemies
        """
        alive_enemies = list[Character]()
        for enemy in self._enemies:
            if enemy.hp > 0:
                alive_enemies.append(enemy)
        return alive_enemies

    def get_alive_players(self) -> list[Character]:
        """
        Return all players with hp > 0
        :return: list of alive players
        """
        alive_players = list[Character]()
        for player in self._players:
            if player.hp > 0:
                alive_players.append(player)
        return alive_players

    def get_character_with_id(self, id: int):
        """
        Searches players and enemy lists for given id
        :param id: id of character that is needed
        :return: Character object if found
        """
        # Look for given id among players
        for char in self._players:
            if char.id == id:
                return char
        # ...and enemies
        for char in self._enemies:
            if char.id == id:
                return char
        return None

    # Private

    def _create_new_view(self, new_turn):
        """
        Creates new view for combat, this can be used in mid-fight
        :param new_turn: id of character with next turn
        :return:
        """
        next_character = self.get_character_with_id(new_turn)

        # Create new view
        self._combat_view = views.concrete.view_combat.ViewCombat(next_character, self._outcomes)

        # Prepare targets
        prepared_targets = self._prepare_strings_for_targets(self.get_alive_enemies())
        self._combat_view.set_targets(prepared_targets)

        # Reload view
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
        context.GAME.view_manager.set_current(Views.COMBAT)

    # Static

    @staticmethod
    def _prepare_strings_for_targets(targets):
        ready_targets = []
        for target in targets:
            ready_targets.append("{name}[{id}]".format(name=target.name, id=target.id))
        return ready_targets


def end_battle(is_won: bool):
    """
    Ends the battle with defeat / win
    :param is_won:
    :return:
    """
    view_manager = context.GAME.view_manager
    context.GAME.combat = None
    if is_won:
        context.GAME.current_room.clear_enemies()
        view_manager.set_new_view_for_enum(Views.ROOM, ViewRoom(context.GAME.current_room))
        view_manager.set_current(Views.ROOM)
    else:
        view_manager.set_new_view_for_enum(Views.DEFEAT, ViewDefeat())
        view_manager.set_current(Views.DEFEAT)
