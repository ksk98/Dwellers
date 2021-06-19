import context
from dungeon.room import Room
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewCombat(ViewBase):
    def __init__(self, my_turn: bool):
        super().__init__()
        self._my_turn = my_turn
        self.options = [
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]
        if self._my_turn:
            self.inputs = {
                "ATTACK TYPE": [0, ["SLASH", "CRUSH", "FIRE", "HEALING"]]
            }
            self.options.insert(0, ["ATTACK", None, lambda: None, Input.SELECT])
            self.options.insert(0, ["ATTACK TYPE", None, lambda: None, Input.MULTI_TOGGLE])

    def print_screen(self):
        print()
        print_whole_line_of_char('=', settings["MAX_WIDTH"])

        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            player_list.append(participant.character.name)

        enemies = context.GAME.current_room.get_enemies()
        enemy_list = ["HOSTILES:"]
        for enemy in enemies:
            enemy_list.append(enemy.name)

        print_in_two_columns([player_list, enemy_list], settings["MAX_WIDTH"])
        print_whole_line_of_char('=', settings["MAX_WIDTH"])
        print()

        # if self._notify_cant_go:
        #     print("Only host can decide when the party is going to the next room!".center(settings["MAX_WIDTH"]))
        #     self._notify_cant_go = False

        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

