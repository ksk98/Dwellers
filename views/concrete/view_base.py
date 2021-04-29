from abc import ABC
from os import system, name
from config import config
import context


class ViewBase(ABC):
    """
    Base class for all of the views implemented in the game.
    """
    def __init__(self):
        self.local_game = context.GAME
        self.selected = 0
        self.options = [
            ("SAMPLE OPTION", None, lambda: None)
        ]

    @staticmethod
    def _clear():
        """
        Clear the terminals window.
        """
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def scroll_up(self):
        """
        Select the option higher than the currently selected. If the
        current option is on the very top just start from the bottom again.
        """
        if self.selected == 0:
            self.selected = len(self.options)-1
        else:
            self.selected -= 1

        self._clear()
        self.print_screen()

    def scroll_down(self):
        """
        Select the option lower than the currently selected. If the
        current option is on the very bottom just start from the top again.
        """
        if self.selected == (len(self.options) - 1):
            self.selected = 0
        else:
            self.selected += 1

        self._clear()
        self.print_screen()

    def _print_options(self):
        """
        Print every selectable option of the view as centered.
        """
        for option in self.options:
            if self.options.index(option) == self.selected:
                print((">" + option[0]).center(config["MAX_WIDTH"]))
            else:
                print(option[0].center(config["MAX_WIDTH"]))

    def execute_current_option(self):
        """
        Executes a function assigned to the currently selected option
        and returns a view to be printed next.
        """
        # In case an out-of-bounds options is selected just ignore the call
        if self.selected < 0 or self.selected > len(self.options)-1:
            return None

        self.options[self.selected][2].__call__()
        return self.options[self.selected][1]
