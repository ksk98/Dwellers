from abc import ABC
from os import system, name
from settings import settings
from views.input_enum import Input
from views.view_enum import Views


class ViewBase(ABC):
    """
    Base class for all of the views implemented in the game.
    """
    def __init__(self):
        self.typing_mode = False
        self.selected = 0
        self.options = [
            ("SAMPLE SELECT OPTION", Views.MENU, lambda: None, Input.SELECT),
            ("SAMPLE TEXT_FIELD OPTION", Views.MENU, lambda: None, Input.TEXT_FIELD)
        ]
        self.text_inputs = {
            "SAMPLE TEXT_FIELD OPTION": "SAMPLE TEXT"
        }

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
        if self.typing_mode:
            return

        if self.selected == 0:
            self.selected = len(self.options)-1
        else:
            self.selected -= 1

    def scroll_down(self):
        """
        Select the option lower than the currently selected. If the
        current option is on the very bottom just start from the top again.
        """
        if self.typing_mode:
            return

        if self.selected == (len(self.options) - 1):
            self.selected = 0
        else:
            self.selected += 1

    def print_screen(self):
        pass

    def _print_options(self):
        """
        Print every selectable option of the view as centered.
        """
        for option in self.options:
            if self.options.index(option) == self.selected:
                print((">" + option[0]).center(settings["MAX_WIDTH"]))
            else:
                print(option[0].center(settings["MAX_WIDTH"]))

    def execute_current_option(self) -> Views:
        """
        Executes a function assigned to the currently selected option
        and returns a view to be printed next.
        """
        # In case an out-of-bounds options is selected just ignore the call
        if self.selected < 0 or self.selected > len(self.options)-1:
            return None

        self.options[self.selected][2].__call__()
        if self.options[self.selected][3] == Input.TEXT_FIELD:
            self.typing_mode = not self.typing_mode
        return self.options[self.selected][1]

    def remove_character_from_current_text_input(self):
        input_name = self.options[self.selected][0]
        input_text = self.text_inputs.get(input_name)
        if input_text != "" or input_text is not None:
            self.text_inputs[input_name] = input_text[0:len(input_text)-2]

    def add_to_current_text_input(self, text: str):
        input_name = self.options[self.selected][0]
        input_text = self.text_inputs.get(input_name)
        if input_text is not None:
            self.text_inputs[input_name] = input_text + text

    def refresh_view(self):
        self._clear()
        self.print_screen()

    def get_index_of_option(self, option: str) -> int:
        for ind in range(len(self.options)):
            if self.options[ind][0] == option:
                return ind

        return -1

    @staticmethod
    def print_text(self, text: str):
        # https://stackoverflow.com/a/18854817
        chunks = list((text[0+i:(settings["MAX_WIDTH"]-4)+i] for i in range(0, len(text), (settings["MAX_WIDTH"]-4))))
        for chunk in chunks:
            print(chunk.center(settings["MAX_WIDTH"]))

