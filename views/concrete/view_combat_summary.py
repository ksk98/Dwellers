import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewCombatSummary(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        # TODO Looted gold sent by server?
        # TODO Number of defeated creatures?
        # TODO IMPLEMENT THIS
        # self.print_multiline_text(                        BATTLE WON BLA BLA BLA
        #     "CONGRATULATIONS!\n \nYOU HAVE REACHED THE END OF A DUNGEON!\nLOOTED GOLD: {0}\n \n".format(
        #         str(context.GAME.gold)))
        self._print_options()

