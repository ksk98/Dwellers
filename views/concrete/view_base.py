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
            ["SAMPLE SELECT OPTION", Views.MENU, lambda: None, Input.SELECT],
            ["SAMPLE TEXT_FIELD OPTION", Views.MENU, lambda: None, Input.TEXT_FIELD]
        ]
        self.inputs = {
            "SAMPLE TEXT OPTION": "SAMPLE TEXT",
            "SAMPLE INT OPTION": 100,
            "SAMPLE BOOLEAN OPTION": True,
            "SAMPLE MULTITOGGLE OPTION": [0, ["OPTION FIRST", "OPTION SECOND", "OPTION THIRD"]]
        }

    @staticmethod
    def clear():
        """
        Clear the terminal's window.
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
        """
        Print the view.
        """
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
        elif self.options[self.selected][3] == Input.TOGGLE:
            self.inputs[self.get_option_for_index(self.selected)] = \
                not self.inputs[self.get_option_for_index(self.selected)]
            self.refresh_view()
        elif self.options[self.selected][3] == Input.MULTI_TOGGLE:
            cur_ind = self.inputs[self.get_option_for_index(self.selected)][0]
            options = self.inputs[self.get_option_for_index(self.selected)][1]
            next_ind = cur_ind + 1
            if next_ind >= len(options):
                next_ind = 0
            self.inputs[self.get_option_for_index(self.selected)][0] = next_ind
        return self.options[self.selected][1]

    def get_input_of_option(self, input_name: str):
        if input_name not in self.inputs:
            return None

        inp = self.inputs[input_name]
        option_index = self.get_index_of_option(input_name)
        if self.options[option_index][3] == Input.MULTI_TOGGLE:
            return inp[1][inp[0]]

        return inp

    def get_input_of_option_index(self, option_index: int):
        return self.get_input_of_option(self.get_option_for_index(option_index))

    def delete_letter(self):
        """
        Perform a backspace in the edited text field.
        """
        input_name = self.options[self.selected][0]
        input_val = self.inputs.get(input_name)
        if input_val is not None and str(input_val) != "":
            if isinstance(input_val, int):
                new_val_str = str(input_val)[0:len(str(input_val)) - 1]
                if new_val_str == "":
                    new_val_str = 0
                self.inputs[input_name] = int(new_val_str)
            else:
                self.inputs[input_name] = input_val[0:len(input_val) - 1]

    def write_letter(self, text: str):
        """
        Write a character to the edited text field.
        """
        input_name = self.options[self.selected][0]
        input_val = self.inputs.get(input_name)
        if input_val is not None:
            if isinstance(input_val, int):
                old_val_str = str(input_val)
                if old_val_str == "0":
                    old_val_str = ""
                self.inputs[input_name] = int(old_val_str + str(text))
            else:
                self.inputs[input_name] = str(input_val) + str(text)

    def refresh_view(self):
        """
        Reprint the view.
        """
        self.clear()
        self.print_screen()

    def get_index_of_option(self, option: str) -> int:
        """
        Get index number of a given option.
        """
        for ind in range(len(self.options)):
            if self.options[ind][0] == option:
                return ind

        return -1

    def get_option_for_index(self, index: int) -> str:
        """
        Get the option assigned to a given index.
        """
        return self.options[index][0]

    def get_view_for_selected(self):
        """
        Get the Views enum assigned to the current option.
        :return:
        """
        return self.options[self.selected][1]

    @staticmethod
    def print_text(text: str):
        """
        Print a given text as centered. If it's too big, break it into several lines.
        """
        # https://stackoverflow.com/a/18854817
        chunks = list((text[0+i:(settings["MAX_WIDTH"]-4)+i] for i in range(0, len(text), (settings["MAX_WIDTH"]-4))))
        for chunk in chunks:
            print(chunk.center(settings["MAX_WIDTH"]))
