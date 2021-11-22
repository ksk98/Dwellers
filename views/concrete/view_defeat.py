import context
from characters.player_factory import PlayerFactory
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewDefeat(ViewBase):
    """
    Screen telling that party has been wiped out
    """
    def __init__(self, character_name: str, outcomes: list[str]):
        super().__init__()
        self.outcomes = outcomes

        # Reset looted gold and killed creatures
        context.GAME.tmp_gold = 0
        context.GAME.defeated_creatures = 0

        PlayerFactory.delete(character_name)

        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        print()
        self.print_outcomes()
        PrintUtility.print_dividing_line()

        self.print_multiline_text("§rDEFEAT!§0\n \n"
                                  "YOU HAVE BEEN WIPED OUT!\n"
                                  "ALL LOOT HAS BEEN LOST...\n ")

        PrintUtility.print_dividing_line()
        print()
        self._print_options()

    def print_outcomes(self):
        # Print last 4 outcomes
        for outcome in self.outcomes[-4:]:
            PrintUtility.print_with_dividing(outcome)
