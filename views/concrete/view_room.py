import context
from dungeon.room import Room
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewRoom(ViewBase):
    def __init__(self, room: Room):
        super().__init__()
        self._notify_cant_go = False
        self._no_rooms_left = False
        self.options = [
            ["GO TO THE NEXT ROOM", Views.ROOM, lambda: self.go_to_next_room(), Input.SELECT],
            ["FLEE", None, lambda: None, Input.SELECT],
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

        # print("Your party:".center(settings["MAX_WIDTH"]))
        # for participant in participants:
        #     player = participant.character
        #     player_string = "[" + str(participant.player_id) + "] " + player.name + " - HP:" + str(player.hp) \
        #                     + " Energy: " + str(player.energy) \
        #                     + " Strength: " + str(player.strength)
        #     print(player_string.center(settings["MAX_WIDTH"]))

        print()
        room = "You are in a " + context.GAME.current_room.get_type().name + " room"
        print(room.center(settings["MAX_WIDTH"]))
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


def print_whole_line_of_char(char: chr, width: int):
    indx = 0
    while indx < width:
        print(char, end='')
        indx += 1
    print()


def print_in_two_columns(column_list: list[list[str]], width: int):
    if len(column_list) == 2:
        left_column_elements = column_list[0]
        right_column_elements = column_list[1]
        for left, right in zip(left_column_elements, right_column_elements):
            elements_length = len(left) + len(right)
            rest = width - elements_length
            if rest > 0:
                print(left, end='')
                for x in range(0, rest):
                    print(' ', end='')
            else:
                print(left)
                for x in range(0, width - len(right)):
                    print(' ', end='')
            print(right)
        if len(left_column_elements) > len(right_column_elements):
            right_len = len(right_column_elements)
            left_len = len(left_column_elements)
            for x in range (right_len, left_len):
                print(left_column_elements[x])
        else:
            right_len = len(right_column_elements)
            left_len = len(left_column_elements)
            for x in range (left_len, right_len):
                for y in range(0, width - len(right_column_elements[x])):
                    print(' ', end='')
                print(right_column_elements[x])
