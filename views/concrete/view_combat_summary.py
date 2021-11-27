import context
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewCombatSummary(ViewBase):
    def __init__(self, outcomes: list[str], enemies_count: int, participant_count: int):
        super().__init__()

        # No. of creatures in completed fight
        self._enemies_count = enemies_count

        # Outcomes of the fight
        self._outcomes = outcomes

        # No. of combat participants - players + enemies
        self._participant_count = participant_count

        # Update stats...
        context.GAME.defeated_creatures += self._enemies_count

        self.options = [
            ["OK", Views.ROOM, lambda: None, Input.SELECT]
        ]

    def print_screen(self):
        print()
        self.print_outcomes()
        PrintUtility.print_dividing_line()

        self.print_multiline_text("§yBATTLE WON!§0\n "
                                  "\n"
                                  "YOU §gSUCCESSFULLY§0 DEFEATED §r{0} ENEMIES§0 AND CAN CONTINUE YOUR JOURNEY.\n "
                                  .format(str(self._enemies_count)))

        PrintUtility.print_dividing_line()
        print()
        self._print_options()

    def print_outcomes(self):
        """
        Prints outcomes that happened since last turn
        """
        outcomes = self._outcomes
        participant_count = self._participant_count

        start_indx = 0
        if len(outcomes) > participant_count:
            start_indx = len(outcomes) - participant_count

        for x in range(start_indx, len(outcomes)):
            PrintUtility.print_with_dividing(outcomes[x])


