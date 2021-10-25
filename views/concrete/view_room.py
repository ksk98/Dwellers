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
        self._notify_cant_go = False
        self._no_rooms_left = False

        if not room.gold_added:
            gold = context.GAME.current_room.get_gold()
            context.GAME.gold += gold
            room.gold_added = True

        self.options = [
            ["LEAVE GAME", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]
        if len(self._room.get_enemies()) > 0 and context.GAME.lobby.local_lobby:
            self.options.insert(0, ["START COMBAT", None, lambda: self.start_combat(), Input.SELECT])
        elif len(self._room.get_enemies()) == 0:
            self.options.insert(0, ["GO TO THE NEXT ROOM", None, lambda: self.go_to_next_room(), Input.SELECT], )

    def print_screen(self):
        print()
        print_whole_line_of_char('=')
        # TODO Combat summary
        self.print_text("Total looted gold: {0}".format(context.GAME.gold))

        self.print_participants()

        print_whole_line_of_char('=')
        gold = context.GAME.current_room.get_gold()
        gold_amount = str(gold) if gold > 0 else "no"

        self.print_multiline_text("You are in a {room_type} room.\n"
                                  "There is {amount} gold in this room.\n"
                                  .format(room_type=context.GAME.current_room.get_type().name, amount=gold_amount))

        if len(self._room.get_enemies()) > 0:  # if enemies are present - start combat
            print()
            self.print_multiline_text("There are enemies in this room!\n"
                                      "Wait for the host to start the battle...\n\n")

        if self._notify_cant_go:
            print("Only host can decide when the party is going to the next room!".center(settings["MAX_WIDTH"]))
            self._notify_cant_go = False
        self._print_options()

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
