import context
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewRoom(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["GO TO THE NEXT ROOM", None, lambda: None, Input.TEXT_FIELD],
            ["FLEE", None, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        participants = context.GAME.lobby.participants
        print("Your party:".center(settings["MAX_WIDTH"]))
        for participant in participants:
            player = participant.character
            player_string = "[" + str(participant.player_id) + "] " + player.name + " - HP:" + str(player.hp) \
                            + " Energy: " + str(player.energy) \
                            + " Strength: " + str(player.strength)
            print(player_string.center(settings["MAX_WIDTH"]))
            print(player_string.center(settings["MAX_WIDTH"]))
            print(player_string.center(settings["MAX_WIDTH"]))
            print()

        print("You are in an empty room".center(settings["MAX_WIDTH"]))

        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))
