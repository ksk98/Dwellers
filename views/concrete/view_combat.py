import context
from characters.character import Character
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


# TODO CANNOT HOST ANOTHER GAME AFTER LEAVING DURING COMBAT
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

        # If it's my turn - display more buttons
        self._my_turn = False
        if self._char_with_turn.id == self._my_character.id:
            self._my_turn = True

        # Combat object
        self._combat = context.GAME.combat
        self.options = [
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]
        if self._my_turn:
            # get attack names
            attacks = context.GAME.lobby.get_local_participant().character.attacks
            attack_names=[]
            for attack in attacks:
                option_name = "{attack_name} [COST: {cost}]".format(attack_name=attack.name, cost=attack.cost)
                attack_names.append(option_name)

            self.inputs = {
                "ATTACK TYPE": [0, attack_names]
            }
            self.options.insert(0, ["REST", None, lambda: self._combat.rest(), Input.SELECT])
            self.options.insert(0, ["ATTACK", None, lambda: self._combat.attack(), Input.SELECT])
            self.options.insert(0, ["ATTACK TYPE", Views.COMBAT, lambda: self._combat.set_target_list_for_attack(),
                                    Input.MULTI_TOGGLE])
            self.options.insert(0, ["TARGET", Views.COMBAT, lambda: None, Input.MULTI_TOGGLE])

    def print_screen(self):
        print()
        self.print_outcomes(self._outcomes)
        print_whole_line_of_char('=')

        # Print party
        player_list, enemy_list = self.prepare_participants()
        print_in_two_columns([player_list, enemy_list])

        print_whole_line_of_char('=')
        print()

        # Print turn
        if not self._my_turn:
            turn = "This is " + self._char_with_turn.name + "'s turn!"
        else:
            turn = "This is your turn!"
        self.print_text(turn)

        if not self._enough_energy:
            self.print_text("You don't have enough energy to do that!")
            self._enough_energy = True

        self._print_options()

    def set_targets(self, list_of_targets):
        """
        Sets the list displaying under "TARGET" option
        :param list_of_targets: list to display
        """
        self.inputs["TARGET"] = [0, list_of_targets]

    def not_enough_energy(self):
        """
        Displays info about not enough energy
        :return:
        """
        self._enough_energy = False
        self.refresh_view()

    def prepare_participants(self):
        """
        Makes two lists of participants - player characters and enemies.
        Lists contain strings telling character's name and it's stats.
        :return: those lists
        """
        participants = self._players
        player_list = ["PARTY:"]
        for character in participants:
            # character = participant.character
            line = "{0}[{1}] - HP:{2}/{3} ENERGY: {4}/{5}" \
                .format(
                    character.name,
                    character.id,
                    str(character.hp),
                    str(character.base_hp),
                    str(character.energy),
                    str(character.base_energy))

            player_list.append(line)

        enemies = self._enemies
        enemy_list = ["HOSTILES:"]
        for enemy in enemies:
            line = "HP:{0}/{1} ENERGY: {2}/{3} - {4}[{5}]"\
                .format(
                    str(enemy.hp),
                    str(enemy.base_hp),
                    str(enemy.energy),
                    str(enemy.base_energy),
                    enemy.name,
                    enemy.id)

            enemy_list.append(line)

        return player_list, enemy_list

    def print_outcomes(self, outcomes: list[str]):
        """
        Prints outcomes that happened since last turn
        :param outcomes: list of all outcomes
        """
        # TODO print more outcomes
        # queue = []
        participant_count = len(self._enemies) + len(self._players)

        start_indx = 0
        if len(outcomes) > participant_count:
            start_indx = len(outcomes) - participant_count

        for x in range(start_indx, len(outcomes)):
            print(outcomes[x])
