import context
from characters.player_factory import PlayerFactory
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import print_whole_line_of_char, print_in_two_columns
from views.view_enum import Views


class ViewGameSummary(ViewBase):
    def __init__(self, take: float, host_take: float):
        super().__init__()

        self.take = take
        self.host_take = host_take
        self.gold = context.GAME.tmp_gold
        self.creatures = context.GAME.defeated_creatures
        self.character = context.GAME.lobby.get_local_participant().character

        # Collect it
        if context.GAME.is_local():
            self.character.gold += self.host_take
        else:
            self.character.gold += self.take

        PlayerFactory.save_player(self.character)

        # Reset
        context.GAME.tmp_gold = 0
        context.GAME.defeated_creatures = 0

        self.options = [
            ["OK", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

    def print_screen(self):
        left, right = self._prepare_summary_table()

        self.print_multiline_text(
            "\nCONGRATULATIONS!\n "
            "\n"
            "YOU HAVE REACHED THE END OF A DUNGEON!\n")
        print_whole_line_of_char('=')
        print_in_two_columns([left, right])
        print_whole_line_of_char('=')
        print()
        self._print_options()

    def _prepare_summary_table(self):
        left = ["Rooms visited", "Defeated creatures", "Total gold looted"]
        right = [str(context.GAME.map.room_count),
                 str(self.creatures),
                 str(self.gold)]
        for player in context.GAME.get_players():
            left.append(context.GAME.get_participant_name(player) + "'s take")
            if player.id == 0:
                right.append(str(self.host_take))
            else:
                right.append(str(self.take))
        return left, right
