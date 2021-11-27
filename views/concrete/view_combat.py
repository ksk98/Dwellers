import context
from characters.character import Character
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewCombat(ViewBase):
    def __init__(self, char_with_turn: Character, outcomes: list[str]):
        super().__init__()

        # List of players in game
        self._players = context.GAME.get_players()

        # List of enemies in battle
        self._enemies = context.GAME.combat.get_alive_enemies()

        # List of outcomes - strings containing info about previous turns
        self._outcomes = outcomes

        # Used to display info about not having enough energy to attack when False
        self._enough_energy = True

        # Character of local player
        self._my_character = context.GAME.lobby.get_local_participant().character

        # Id of character currently having turn
        self._char_with_turn = char_with_turn

        # Bool used to display confirmation before leaving the game
        self._confirm_leave = False

        # If it's my turn - display more buttons
        self._my_turn = False
        if self._char_with_turn.id == self._my_character.id:
            self._my_turn = True

        # Combat objects
        self._combat = context.GAME.combat
        self._server_combat = context.GAME.server_combat

        self.options = [
            ["LEAVE GAME", None, lambda: self._leave_game(), Input.SELECT]
        ]
        if self._my_turn:
            # Get attack names
            attacks = context.GAME.lobby.get_local_participant().character.attacks
            attack_names = []
            for attack in attacks:
                option_name = f"{attack.name} [COST: {attack.cost}]"
                attack_names.append(option_name)

            self.inputs = {
                "ATTACK TYPE": [0, attack_names]
            }
            self.options.insert(0, ["REST", None, lambda: self._combat.rest(), Input.SELECT])

            # This shouldn't happen
            # But I will add just in case
            # So client will not crash
            # With this, if there are no enemies the only thing that player can do is rest
            if len(self._enemies) > 0:
                self.options.insert(0, ["ATTACK", None, lambda: self._combat.attack(), Input.SELECT])
                self.options.insert(0, ["ATTACK TYPE", Views.COMBAT, lambda: self._combat.set_target_list_for_attack(),
                                        Input.MULTI_TOGGLE])
                # TODO BUG: can't choose target properly -
                #  right arrow selects last enemy, left arrow selects last friendly
                self.options.insert(0, ["TARGET", Views.COMBAT, lambda: None, Input.MULTI_TOGGLE])
        else:
            self.options.insert(0, ["DO NOTHING", Views.COMBAT, lambda: None, Input.SELECT])

    def print_screen(self):
        print()
        self._print_outcomes(self._outcomes)
        PrintUtility.print_dividing_line()

        # Print party
        player_list, enemy_list = self._prepare_participants()
        PrintUtility.print_in_columns([player_list, enemy_list], equal_size=True)

        PrintUtility.print_dividing_line()
        print()

        # This should be set to True only shortly after pressing the LEAVE GAME button
        # so it needs to be changed with next refresh
        self._confirm_leave = False

        self._print_turn_text()

        self._print_energy_alert()

        # Options
        self._print_options()

    def _print_energy_alert(self):
        # Energy info
        if not self._enough_energy:
            self.print_text("§yYou don't have enough energy to do that!§0")
            self._enough_energy = True

    def _print_turn_text(self):
        # Print turn
        if not self._my_turn:
            turn = "This is §g" + context.GAME.get_participant_name(self._char_with_turn) + "§0's turn!"
            if self._combat.am_i_dead():
                turn += "\n§rLooks like you're dead! Ask your friends to heal you!§0"
        else:
            turn = "This is §Gyour§0 turn!"
        self.print_multiline_text(turn)

    def handle_arrow_left(self):
        self._combat.set_target_list_for_attack(previous_attack_not_next=True)
        super().handle_arrow_left()

    def handle_arrow_right(self):
        self._combat.set_target_list_for_attack()
        super().handle_arrow_right()

    def not_enough_energy(self):
        """
        Displays info about not enough energy
        :return:
        """
        self._enough_energy = False
        self.refresh_view()

    def set_targets(self, list_of_targets):
        """
        Sets the list displaying under "TARGET" option
        :param list_of_targets: list to display
        """
        self.inputs["TARGET"] = [0, list_of_targets]

    def _prepare_participants(self):
        """
        Makes two lists of participants - player characters and enemies.
        Lists contain strings telling character's name and it's stats.
        :return: those lists
        """
        player_list = self._create_character_list(self._players, ["PARTY:"], "§g")

        enemy_list = self._create_character_list(self._enemies, ["HOSTILES:"], "§y")

        return player_list, enemy_list

    def _print_outcomes(self, outcomes: list[str]):
        """
        Prints outcomes that happened since last turn
        :param outcomes: list of all outcomes
        """
        participant_count = len(self._enemies) + len(self._players)

        start_indx = 0
        if len(outcomes) > participant_count:
            start_indx = len(outcomes) - participant_count

        for x in range(start_indx, len(outcomes)):
            PrintUtility.print_with_dividing(outcomes[x])

    def _leave_game(self):
        """
        Displays confirmation and leaves game
        """
        if self._confirm_leave:
            context.GAME.abandon_lobby()
            context.GAME.view_manager.set_current(Views.MENU)
        else:
            self._confirm_leave = True
            self.print_text("§rDo you really want to leave your friends?§0")

    @staticmethod
    def _create_character_list(characters, character_list, color):
        for character in characters:
            name = f"{color}{context.GAME.get_participant_name(character)}§0[{character.id}]"
            stats = f"§rHP:§R {str(character.hp)}§r/{str(character.get_base_hp())}§0 " \
                    f"§bEP:§B {str(character.energy)}§b/{str(character.get_base_energy())}§0"

            character_list.append(name)
            character_list.append(stats)
            character_list.append("")
        return character_list
