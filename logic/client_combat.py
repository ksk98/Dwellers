import context
import views.concrete.view_combat
from characters.character import Character
from characters.hit import Hit
from network import communication
from views.concrete.view_combat_summary import ViewCombatSummary
from views.concrete.view_defeat import ViewDefeat
from views.concrete.view_room import ViewRoom
from views.view_enum import Views


class ClientCombat:
    """
    Controls CombatView based on player / enemy characters and received data from host
    """
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

        # Get attack
        attack_index = self._combat_view.inputs.get("ATTACK TYPE")[0]
        attack = self.get_character_with_id(self._my_id).attacks[attack_index].name

        # Choose target list based on selected attack
        if attack == "Heal":
            targets = self._players
        else:
            targets = self.get_alive_enemies()

        # Get target from list
        target_index = self._combat_view.inputs.get("TARGET")[0]
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
            context.GAME.server_combat.act()

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
                user.deal_energy_damage(hit.energy_cost)

            self.create_new_view(new_turn)

    def prepare_combat_summary(self):
        """
        Creates view of combat summary
        """
        participant_count = len(self.get_alive_enemies()) + len(self.get_alive_players())
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT_SUMMARY,
                                                        ViewCombatSummary(self._outcomes,
                                                                          len(self._enemies),
                                                                          participant_count))

    def restore_energy(self):
        """
        Restores energy of all players after the fight
        """
        for player in self._players:
            player.energy = player.get_base_energy()

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
            context.GAME.server_combat.act()

    def set_target_list_for_attack(self, previous_attack_not_next=False):
        """
        Sets the targets in CombatView based on selected attack type (heal - players and enemies otherwise)
        """

        # Get attack string (with cost)
        attack_string: str
        if not previous_attack_not_next:
            attack_string = self._combat_view.get_input_of_next_option("ATTACK TYPE")
        else:
            attack_string = self._combat_view.get_input_of_previous_option("ATTACK TYPE")
        # Search attacks for this attack
        for att in self.get_character_with_id(self._my_id).attacks:
            if att.name in attack_string:
                # Override it
                attack_string = att.name
                break

        if attack_string == "Heal":
            prepared_targets = self._prepare_strings_for_targets(self._players)
            self._combat_view.set_targets(prepared_targets)
        else:
            prepared_targets = self._prepare_strings_for_targets(self.get_alive_enemies())
            self._combat_view.set_targets(prepared_targets)

    # Getters

    def start(self):
        """
        Starts the combat - sets the view
        """
        self.create_new_view(self._id_with_turn)

    def am_i_dead(self):
        """
        Returns information if local player is dead
        :return: true if local player is dead
        """
        my_character = self.get_character_with_id(self._my_id)
        if my_character.hp > 0:
            return False
        return True

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

    def get_outcomes(self) -> list[str]:
        return self._outcomes

    # Static

    def create_new_view(self, new_turn: int = -1):
        """
        Creates new view for combat, this can be used in mid-fight
        :param new_turn: id of character with next turn
        :return:
        """
        # Same as the previous turn (reload whole view)
        if new_turn == -1:
            new_turn = self._id_with_turn

        next_character = self.get_character_with_id(new_turn)

        # Create new view
        self._combat_view = views.concrete.view_combat.ViewCombat(next_character, self._outcomes)

        # Prepare targets
        prepared_targets = self._prepare_strings_for_targets(self.get_alive_enemies())
        self._combat_view.set_targets(prepared_targets)

        # Reload view
        context.GAME.view_manager.set_new_view_for_enum(Views.COMBAT, self._combat_view)
        context.GAME.view_manager.set_current(Views.COMBAT)

    @staticmethod
    def _prepare_strings_for_targets(targets):
        ready_targets = []
        for target in targets:
            ready_targets.append("{name}[{id}]".format(
                name=context.GAME.get_participant_name(target),
                id=target.id))
        return ready_targets


def end_battle(is_won: bool):
    """
    Ends the battle with defeat / win
    :param is_won:
    :return:
    """
    view_manager = context.GAME.view_manager
    if is_won:
        # Create view of game summary
        context.GAME.combat.prepare_combat_summary()

        # Clean variables
        context.GAME.combat = None
        context.GAME.current_room.clear_enemies()

        # Prepare view for room (displayed after summary)
        view_manager.set_new_view_for_enum(Views.ROOM, ViewRoom(context.GAME.current_room))
        # And change view to summary
        view_manager.set_current(Views.COMBAT_SUMMARY)
    else:
        # Get necessary variables
        character_name = context.GAME.lobby.get_local_participant().name
        outcomes = context.GAME.combat.get_outcomes()
        # Clear combat
        context.GAME.combat = None
        # Change view
        view_manager.set_new_view_for_enum(Views.DEFEAT, ViewDefeat(character_name, outcomes))
        view_manager.set_current(Views.DEFEAT)
