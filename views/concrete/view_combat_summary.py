import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char
from views.view_enum import Views


class ViewCombatSummary(ViewBase):
    def __init__(self, outcomes: list[str], enemies_count: int, participant_count: int):
        super().__init__()
        self._enemies_count = enemies_count
        self._outcomes = outcomes
        self._participant_count = participant_count
        self.options = [
            ["OK", Views.ROOM, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        print()
        self.print_outcomes()
        print_whole_line_of_char('=')

        self.print_multiline_text(
            "BATTLE WON!\n \nYOU SUCCESSFULLY DEFEATED {0} ENEMIES AND CAN CONTINUE YOUR JOURNEY.\n \n".format(
                str(self._enemies_count)))

        print_whole_line_of_char('=')
        print()
        self._print_options()

    def print_outcomes(self):
        """
        Prints outcomes that happened since last turn
        :param outcomes: list of all outcomes
        """
        outcomes = self._outcomes
        participant_count = self._participant_count

        start_indx = 0
        if len(outcomes) > participant_count:
            start_indx = len(outcomes) - participant_count

        for x in range(start_indx, len(outcomes)):
            print(outcomes[x])


