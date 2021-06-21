import context
from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_slash import AttackSlash
from settings import settings
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
                "ATTACK TYPE": [0, ["SLASH", "CRUSH", "FIRE"]]
            }
            self.options.insert(0, ["REST", None, lambda: self.rest(), Input.SELECT])
            self.options.insert(0, ["ATTACK", None, lambda: self.attack(), Input.SELECT])
            self.options.insert(0, ["ATTACK TYPE", Views.COMBAT, lambda: None, Input.MULTI_TOGGLE])

    def print_screen(self):
        print()
        self.print_outcomes(self._outcomes)
        print_whole_line_of_char('=', settings["MAX_WIDTH"])

        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            character = participant.character
            line = character.name + " -" \
                     + " HP:" + str(character.hp) + "/" + str(character.base_hp) \
                     + " ENERGY:" + str(character.energy) + "/" + str(character.base_energy)
            player_list.append(line)

        enemies = context.GAME.combat.get_alive_enemies()
        enemy_list = ["HOSTILES:"]
        for enemy in enemies:
            line = " HP:" + str(enemy.hp) + "/" + str(enemy.base_hp) \
                   + " ENERGY:" + str(enemy.energy) + "/" + str(enemy.base_energy) \
                   + " - " + enemy.name
            enemy_list.append(line)

        print_in_two_columns([player_list, enemy_list], settings["MAX_WIDTH"])
        print_whole_line_of_char('=', settings["MAX_WIDTH"])
        print()

        if not self._my_turn:
            character_with_turn = context.GAME.combat.get_current_character_name()
            line = "This is " + character_with_turn + "'s turn!"
        else:
            line = "This is your turn!"
        print(line.center(settings["MAX_WIDTH"]))

        if not self._enough_energy:
            print("You don't have enough energy to do that!".center(settings["MAX_WIDTH"]))
            self._enough_energy = True

        for option in self.options:
            to_print = option[0]
            value = self.get_input_of_option(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

    def print_outcomes(self, outcomes: list[str]):
        """
        Used to print last 4 outcomes
        :param outcomes:
        :return:
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
        character = context.GAME.lobby.get_local_participant().character
        combat = context.GAME.combat
        outcome = "ERR"
        if len(combat.get_alive_enemies()) > 0:
            if self.get_input_of_option("ATTACK TYPE") == "SLASH":
                outcome = character.use_skill_on(AttackSlash(), combat.get_alive_enemies()[0])
            elif self.get_input_of_option("ATTACK TYPE") == "CRUSH":
                outcome = character.use_skill_on(AttackCrush(), combat.get_alive_enemies()[0])
            elif self.get_input_of_option("ATTACK TYPE") == "FIRE":
                outcome = character.use_skill_on(AttackFire(), combat.get_alive_enemies()[0])
        if outcome == "":
            self._enough_energy = False
            context.GAME.view_manager.refresh()
        else:
            combat.add_outcome(outcome)
            combat.end_turn()

    def rest(self):
        character = context.GAME.lobby.get_local_participant().character
        combat = context.GAME.combat
        outcome = character.rest()
        combat.add_outcome(outcome)
        combat.end_turn()
