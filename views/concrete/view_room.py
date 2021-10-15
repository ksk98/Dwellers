import context
from dungeon.room import Room
from logic.combat import Combat
from network.communication import communicate
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_game_summary import ViewGameSummary
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewRoom(ViewBase):
    def __init__(self, room: Room):
        super().__init__()
        self._room = room
        self._notify_cant_go = False
        self._no_rooms_left = False

        if not room.gold_added:
            gold = context.GAME.current_room.get_gold()
            context.GAME.gold += gold
            room.gold_added = True

        self.options = [
            ["GO TO THE NEXT ROOM", Views.ROOM, lambda: self.go_to_next_room(), Input.SELECT],
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        if len(self._room.get_enemies()) > 0:  # if enemies are present - start combat
            context.GAME.combat = Combat(context.GAME.get_players(), self._room.get_enemies())
            context.GAME.combat.start()
        else:
            print()
            print_whole_line_of_char('=')

            self.print_participants()

            print_whole_line_of_char('=')
            gold = context.GAME.current_room.get_gold()
            gold_amount = str(gold) if gold > 0 else "no"

            self.print_multiline_text("You are in a {room_type} room.\n"
                                      "There is {amount} gold in this room.\n \n"
                                      .format(room_type=context.GAME.current_room.get_type().name, amount=gold_amount))

            context.GAME.gold += gold
            print()

            if self._notify_cant_go:
                print("Only host can decide when the party is going to the next room!".center(settings["MAX_WIDTH"]))
                self._notify_cant_go = False

            self.check_end()

            self._print_options()

    def check_end(self):
        if self._no_rooms_left:
            if context.GAME.lobby.local_lobby:
                for client in context.GAME.sockets.values():
                    communicate(client, ["GAMEPLAY", "ACTION:END"])
            context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary())
            context.GAME.view_manager.set_current(Views.SUMMARY)

    def print_participants(self):
        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            player_list.append(participant.character.name)
        print_in_two_columns([player_list, [""]])

    def go_to_next_room(self):
        if context.GAME.lobby.local_lobby:
            if not context.GAME.current_room.has_next():
                self._no_rooms_left = True
            context.GAME.send_next_room_action()
        else:
            self._notify_cant_go = True
