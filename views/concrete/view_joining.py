from views.concrete.view_base import ViewBase


class ViewJoining(ViewBase):
    def __init__(self, current_state: str):
        super().__init__()
        self.current_state = current_state
        self.options = []

    def print_screen(self):
        self._print_logo()
        self.print_text(self.current_state)
        self._print_options()
