from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewJoining(ViewBase):
    def __init__(self):
        super().__init__()
        self.options = [
            ("CANCEL", None, lambda: None, Input.SELECT)    # TODO
        ]

    def print_screen(self):
        self.print_text("CONNECTING...")
        self._print_options()
