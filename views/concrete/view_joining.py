from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewJoining(ViewBase):
    def __init__(self, current_state: str):
        super().__init__()
        self.current_state = current_state
        self.options = [
            ["CANCEL", Views.JOIN, lambda: None, Input.SELECT]    # TODO
        ]

    def print_screen(self):
        self.print_text(self.current_state)
        self._print_options()
