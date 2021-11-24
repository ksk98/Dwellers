import os

import context
from settings import settings
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewSettings(ViewBase):
    """
    Setting view (duh)
    """
    def __init__(self):
        super().__init__()

        self.options = []
        self.inputs = {}
        self.selected_character = settings["SELECTED_CHARACTER"]

        for setting in settings:
            if setting == "SELECTED_CHARACTER":
                continue

            if setting == "INTERFACE_COLOR":
                # All this is necessary, because all other views work different than settings view
                # List of available colors
                colors = ["BLUE", "CYAN", "GREEN", "YELLOW"]
                # Add button
                self.options.append([setting, None, lambda: None, Input.MULTI_TOGGLE])
                # Get saved color
                color_indx = indx = settings[setting][0]
                bc = settings[setting][1][indx]
                # Set button to selected color
                self.inputs[setting] = [color_indx, colors]
                continue

            if isinstance(settings[setting], bool):
                self.options.append([setting, None, lambda: None, Input.TOGGLE])
            else:
                self.options.append([setting, None, lambda: None, Input.TEXT_FIELD])

            self.inputs[setting] = settings[setting]

        self.options.append(["BACK TO MENU", Views.MENU, lambda: self.update_settings(), Input.SELECT])

    def update_settings(self):
        for setting in self.inputs:
            settings[setting] = self.inputs[setting]
        context.GAME.save_settings()
        os.system('mode con: cols=' + str(settings["MAX_WIDTH"]) + ' lines=25')

    def print_screen(self):
        self._print_logo()
        self._print_options()
