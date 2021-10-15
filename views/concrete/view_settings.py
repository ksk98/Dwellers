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
        self._print_logo()
        self._print_options()
