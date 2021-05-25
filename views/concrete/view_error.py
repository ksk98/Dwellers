from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewError(ViewBase):
    def __init__(self, return_to: Views = Views.MENU, error_text: str = ""):
        super().__init__()
        self.text = error_text
        self.options = [
            ("OK", return_to, lambda: None, Input.SELECT)
        ]

    def print_screen(self):
        self.print_text(self.text)
