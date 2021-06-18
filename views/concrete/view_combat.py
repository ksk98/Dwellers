import context
from dungeon.room import Room
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewCombat(ViewBase):
    def __init__(self):
        super().__init__()
        self._notify_cant_go = False
        self._no_rooms_left = False
        self.options = [
            ["ATTACK", None, lambda: None, Input.SELECT],
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

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

        if self._notify_cant_go:
            print("Only host can decide when the party is going to the next room!".center(settings["MAX_WIDTH"]))
            self._notify_cant_go = False
        if self._no_rooms_left:
            print("We have reached the end!".center(settings["MAX_WIDTH"]))
            self._no_rooms_left = False

        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

    def go_to_next_room(self):
        if context.GAME.lobby.local_lobby:
            if not context.GAME.current_room.has_next():
                self._no_rooms_left = True
            context.GAME.send_next_room_action()
        else:
            self._notify_cant_go = True

