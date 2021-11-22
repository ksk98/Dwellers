import context
from characters.player_factory import PlayerFactory
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewGameSummary(ViewBase):
    def __init__(self, take: float):
        super().__init__()

        self.take = take
        self.gold = context.GAME.tmp_gold
        self.creatures = context.GAME.defeated_creatures
        self.character = context.GAME.lobby.get_local_participant().character

        # Collect it
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
            "\n§yCONGRATULATIONS!§0\n "
            "\n"
            "YOU HAVE REACHED THE END OF A DUNGEON!\n")
        PrintUtility.print_dividing_line()
        PrintUtility.print_in_columns([[], left, right], equal_size=True)
        PrintUtility.print_dividing_line()
        print()
        self._print_options()

    def _prepare_summary_table(self):
        left = ["§BRooms§0 visited", "Defeated §rcreatures§0", "Total §ygold§0 looted"]
        right = [str(context.GAME.map.room_count),
                 f"{str(self.creatures)}",
                 f"{str(self.gold)}"]
        for player in context.GAME.get_players():
            left.append(f"§g{context.GAME.get_participant_name(player)}§0's take")
            right.append(f"{str(self.take)}")
        return left, right
