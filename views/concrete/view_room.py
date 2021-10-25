import context
from dungeon.room import Room
from logic.server_combat import ServerCombat
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
        self._confirm_leave = False
        self._notify_cant_go = False
        self._no_rooms_left = False

        if not room.gold_added:
            gold = context.GAME.current_room.get_gold()
            context.GAME.gold += gold
            room.gold_added = True

        self.options = [
            ["LEAVE GAME", None, lambda: self.leave_game(), Input.SELECT]
        ]
        if len(self._room.get_enemies()) > 0 and context.GAME.lobby.local_lobby:
            self.options.insert(0, ["START COMBAT", None, lambda: self.start_combat(), Input.SELECT])
        elif len(self._room.get_enemies()) == 0:
            self.options.insert(0, ["GO TO THE NEXT ROOM", Views.ROOM, lambda: self.go_to_next_room(), Input.SELECT], )
        else:
            self.options.insert(0, ["DO NOTHING", None, lambda: None, Input.SELECT])

    def print_screen(self):
        print()
        print_whole_line_of_char('=')

        self.print_participants()

        print_whole_line_of_char('=')
        gold = context.GAME.current_room.get_gold()
        gold_amount = str(gold) if gold > 0 else "no"

        self.print_multiline_text("You are in a {room_type} room.\n"
                                  "There is {amount} gold in this room.\n"
                                  "Total looted gold: {total_gold}\n"
                                  .format(room_type=context.GAME.current_room.get_type().name, amount=gold_amount, total_gold=context.GAME.gold))

        if len(self._room.get_enemies()) > 0:  # if enemies are present - start combat
            print()
            self.print_text("There are enemies in this room!")
            if not context.GAME.lobby.local_lobby:
                self.print_text("Wait for the host to start the battle...")

        if self._notify_cant_go:
            self.print_text("Only host can decide when the party is going to the next room!")
            self._notify_cant_go = False

        self._print_options()

        if self._confirm_leave:
            self._confirm_leave = False

    def leave_game(self):
        if self._confirm_leave:
            context.GAME.view_manager.set_current(Views.MENU)
            context.GAME.abandon_lobby()
        else:
            self._confirm_leave = True
            self.print_text("Do you really want to abandon your party?")

    def start_combat(self):
        combat = ServerCombat()
        context.GAME.server_combat = combat
        combat.start()

    def print_participants(self):
        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            player_string = "{nick} - HP:{current}/{base}" \
                .format(
                nick=participant.character.name,
                current=participant.character.hp,
                base=participant.character.base_hp)
            player_list.append(player_string)
        print_in_two_columns([player_list, [""]])

    def go_to_next_room(self):
        if context.GAME.lobby.local_lobby:
            has_next = context.GAME.current_room.has_next()
            context.GAME.send_next_room_action()
            if has_next:
                context.GAME.go_to_the_next_room()
            else:
                context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary())
                context.GAME.view_manager.set_current(Views.SUMMARY)
        else:
            self._notify_cant_go = True
