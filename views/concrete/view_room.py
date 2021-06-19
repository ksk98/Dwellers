import context
from dungeon.room import Room
from logic.combat import Combat
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_game_summary import ViewGameSummary
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewRoom(ViewBase):
    def __init__(self, room: Room):
        super().__init__()
        if len(room.get_enemies()) > 0:
            context.GAME.combat = Combat(context.GAME.get_players(), room.get_enemies())
            context.GAME.combat.start()
        self._notify_cant_go = False
        self._no_rooms_left = False
        self.options = [
            ["GO TO THE NEXT ROOM", Views.ROOM, lambda: self.go_to_next_room(), Input.SELECT],
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
        enemy_list = [""]

        print_in_two_columns([player_list, enemy_list], settings["MAX_WIDTH"])
        print_whole_line_of_char('=', settings["MAX_WIDTH"])

        line = "You are in a " + context.GAME.current_room.get_type().name + " room."
        print(line.center(settings["MAX_WIDTH"]))
        gold = context.GAME.current_room.get_gold()
        if gold > 0:
            line = "There is " + str(gold) + " gold in this room!"
        else:
            line = "There is no gold in this room :("
        context.GAME.gold += gold
        print(line.center(settings["MAX_WIDTH"]))
        print()

        if self._notify_cant_go:
            print("Only host can decide when the party is going to the next room!".center(settings["MAX_WIDTH"]))
            self._notify_cant_go = False
        if self._no_rooms_left:
            context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary())
            context.GAME.view_manager.set_current(Views.SUMMARY)
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
