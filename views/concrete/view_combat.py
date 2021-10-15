import context
from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_heal import AttackHeal
from characters.attacks.attack_slash import AttackSlash
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewCombat(ViewBase):
    def __init__(self, my_turn: bool, outcomes: list[str]):
        super().__init__()
        self._outcomes = outcomes
        self._my_turn = my_turn
        self._enough_energy = True
        self.options = [
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]
        if self._my_turn:
            self.inputs = {
                "ATTACK TYPE": [0, ["SLASH", "CRUSH", "FIRE", "HEAL"]]
            }
            self.options.insert(0, ["REST", None, lambda: self.rest(), Input.SELECT])
            self.options.insert(0, ["ATTACK", None, lambda: self.attack(), Input.SELECT])
            self.options.insert(0, ["ATTACK TYPE", Views.COMBAT, lambda: self.set_target_list_for_attack(),
                                    Input.MULTI_TOGGLE])
            # TODO add id to target's name
            self.options.insert(0, ["TARGET", Views.COMBAT, lambda: None, Input.MULTI_TOGGLE])
            self.set_targets_input_to_enemies()

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
            character_with_turn = context.GAME.combat.get_current_character_name()
            turn = "This is " + character_with_turn + "'s turn!"
        else:
            turn = "This is your turn!"
        self.print_text(turn)

        if not self._enough_energy:
            self.print_text("You don't have enough energy to do that!")
            self._enough_energy = True

        self._print_options()

    def set_targets_input_to_enemies(self):
        alive_enemies = []
        for enemy in context.GAME.combat.get_alive_enemies():
            alive_enemies.append(enemy.name)
        self.inputs["TARGET"] = [0, alive_enemies]
        self.refresh_view()

    def set_targets_input_to_friendlies(self):
        alive_players = []
        for friendly in context.GAME.combat.get_alive_players():
            alive_players.append(friendly.name)
        self.inputs["TARGET"] = [0, alive_players]
        self.refresh_view()

    def set_target_list_for_attack(self):
        attack = self.get_input_of_next_option("ATTACK TYPE")
        if attack is None:
            return

        if attack == "HEAL":
            self.set_targets_input_to_friendlies()
        else:
            if self.get_input_of_option("ATTACK TYPE") == "HEAL":
                self.set_targets_input_to_enemies()

    def print_outcomes(self, outcomes: list[str]):
        """
        Used to print last 4 outcomes
        :param outcomes: list of all outcomes
        """
        queue = []
        size = 0
        for outcome in outcomes:
            queue.append(outcome)
            if size >= 4:
                queue.pop(0)
            size += 1

        for outcome in queue:
            print(outcome)

    def attack(self):
        """
        Take attack type from input and attack selected character
        """
        character = context.GAME.lobby.get_local_participant().character
        combat = context.GAME.combat
        outcome = "ERR"
        if len(combat.get_alive_enemies()) > 0:
            target_index = self.inputs["TARGET"][0]
            attack_type = self.get_input_of_option("ATTACK TYPE")
            enemy = combat.get_alive_enemies()[target_index]

            attack = None  # TODO display cost of each attack
            attack = {
                "SLASH": AttackSlash(),
                "CRUSH": AttackCrush(),
                "HEAL": AttackHeal(),
                "FIRE": AttackFire()
            }[attack_type]

            if attack:
                outcome = character.use_skill_on(attack, enemy)

        if outcome == "":
            self._enough_energy = False
            context.GAME.view_manager.refresh()
        else:
            combat.add_outcome(outcome)
            combat.end_turn()

    @staticmethod
    def rest():
        """
        Rest action for character. Uses character.rest() on player's character and adds outcome.
        """
        character = context.GAME.lobby.get_local_participant().character
        combat = context.GAME.combat
        outcome = character.rest()
        combat.add_outcome(outcome)
        combat.end_turn()

    @staticmethod
    def prepare_participants():
        """
        Makes two lists of participants - player characters and enemies.
        Lists contain strings telling character's name and it's stats.
        :return: those lists
        """
        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            character = participant.character
            line = "{0} - HP:{1}/{2} ENERGY: {3}/{4}" \
                .format(
                    character.name,
                    str(character.hp),
                    str(character.base_hp),
                    str(character.energy),
                    str(character.base_energy))

            player_list.append(line)

        enemies = context.GAME.combat.get_alive_enemies()
        enemy_list = ["HOSTILES:"]
        for enemy in enemies:
            line = "HP:{0}/{1} ENERGY: {2}/{3} - {4}"\
                .format(
                    str(enemy.hp),
                    str(enemy.base_hp),
                    str(enemy.energy),
                    str(enemy.base_energy),
                    enemy.name)

            enemy_list.append(line)

        return player_list, enemy_list