import context
from characters.player_factory import PlayerFactory
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char
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
        self.print_outcomes()
        print_whole_line_of_char('=')
        self.print_multiline_text("DEFEAT!\n \n"
                                  "YOU HAVE BEEN WIPED OUT!\n"
                                  "ALL LOOT HAS BEEN LOST...")
        print_whole_line_of_char('=')
        print()
        self._print_options()

    def print_outcomes(self):
        # Print last 4 outcomes
        for outcome in self.outcomes[-4:]:
            print(outcome)
