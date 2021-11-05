import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewError(ViewBase):
    def __init__(self, error_text: str = "", return_to: Views = Views.MENU):
        super().__init__()
        self.text = error_text
        self.options = [
            ["OK", return_to, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        self.print_text("ERROR:")
        self.print_text(self.text)
        print()
        self._print_options()

    @staticmethod
    def _action(return_to):
        context.GAME.view_manager.view_overridden_by_error = True
