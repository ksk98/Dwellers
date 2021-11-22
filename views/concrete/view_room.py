import context
from dungeon.room import Room
from logic.server_combat import ServerCombat
from views.concrete.view_base import ViewBase
from views.concrete.view_game_summary import ViewGameSummary
from views.input_enum import Input
from views.print_utility import PrintUtility
from views.view_enum import Views


class ViewRoom(ViewBase):
    def __init__(self, room: Room):
        super().__init__()
        self._room = room
        self._confirm_leave = False
        self._notify_cant_go = False
        self._no_rooms_left = False

        # Add gold with the first visit
        if not room.gold_added:
            gold = context.GAME.current_room.get_gold()
            context.GAME.tmp_gold += gold
            room.gold_added = True

        self.options = [
            ["LEAVE GAME", None, lambda: self._leave_game(), Input.SELECT]
        ]
        # Add buttons to start combat or go to the next room
        if len(self._room.get_enemies()) > 0 and context.GAME.lobby.local_lobby:
            self.options.insert(0, ["START COMBAT", None, lambda: self._start_combat(), Input.SELECT])
        elif len(self._room.get_enemies()) == 0:
            self.options.insert(0, ["GO TO THE NEXT ROOM", None, lambda: self._go_to_next_room(), Input.SELECT], )
        else:
            self.options.insert(0, ["DO NOTHING", None, lambda: None, Input.SELECT])

    def print_screen(self):
        print()
        PrintUtility.print_dividing_line()

        self._print_participants()

        PrintUtility.print_dividing_line()

        # Get gold
        gold = context.GAME.current_room.get_gold()
        gold_amount = str(gold) if gold > 0 else "no"

        # Print short description
        self.print_multiline_text("You are in a §c{room_type}§0 room.\n"
                                  "There is §y{amount} gold§0 in this room.\n"
                                  "Total looted gold: §y{total_gold}§0\n \n"
                                  .format(room_type=context.GAME.current_room.get_type().name,
                                          amount=gold_amount,
                                          total_gold=context.GAME.tmp_gold))

        if len(self._room.get_enemies()) > 0:  # if enemies are present - start combat
            self.print_text("§rThere are enemies in this room!§0")
            if not context.GAME.lobby.local_lobby:
                self.print_text("§yWait for the host to start the battle...§0")

        # Notify player that only host can move between rooms
        if self._notify_cant_go:
            self.print_text("§yOnly host can decide when the party is going to the next room!§0")
            self._notify_cant_go = False

        self._print_options()

        if self._confirm_leave:
            self._confirm_leave = False

    def _leave_game(self):
        """
        Used to display leave confirmation and for leaving.
        """
        if self._confirm_leave:
            context.GAME.view_manager.set_current(Views.MENU)
            context.GAME.abandon_lobby()
        else:
            self._confirm_leave = True
            self.print_text("§rDo you really want to abandon your party?§0")

    def _start_combat(self):
        """
        Starts combat by creating ServerCombat object.
        """
        combat = ServerCombat()
        context.GAME.server_combat = combat
        combat.start()

    def _print_participants(self):
        """
        Prints all players with their stats in a nice column
        """
        participants = context.GAME.lobby.participants
        player_list = ["PARTY:"]
        for participant in participants:
            name = f"§g{context.GAME.get_participant_name(participant.character)}§0[{participant.player_id}]"
            stats = f"§rHP:§R {str(participant.character.hp)}§r/{str(participant.character.get_base_hp())}§0 "

            player_list.append(name)
            player_list.append(stats)
            player_list.append("")
        PrintUtility.print_in_columns([player_list])

    def _go_to_next_room(self):
        """
        Decides if party is going to the next room or that game is won.
        """
        if context.GAME.lobby.local_lobby:
            has_next = context.GAME.current_room.has_next()
            context.GAME.send_next_room_action()
            if has_next:
                context.GAME.go_to_the_next_room()
            else:
                take = context.GAME.calculate_take()
                context.GAME.view_manager.set_new_view_for_enum(Views.SUMMARY, ViewGameSummary(take))
                context.GAME.view_manager.set_current(Views.SUMMARY)
        else:
            self._notify_cant_go = True
