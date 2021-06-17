from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewSettings(ViewBase):
    def __init__(self):
        super().__init__()

        self.options = []
        self.inputs = {}
        self.selected_character = settings["SELECTED_CHARACTER"]

        for setting in settings:
            if setting == "SELECTED_CHARACTER":
                continue
            if isinstance(settings[setting], bool):
                self.options.append([setting, None, lambda: None, Input.TOGGLE])
            else:
                self.options.append([setting, None, lambda: None, Input.TEXT_FIELD])
            self.inputs[setting] = settings[setting]

        self.options.append(["EXIT", Views.MENU, lambda: self.update_settings(), Input.SELECT])

    def update_settings(self):
        for setting in self.inputs:
            settings[setting] = self.inputs[setting]

    def print_screen(self):
        for option in self.options:
            to_print = option[0]
            value = self.inputs.get(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))
