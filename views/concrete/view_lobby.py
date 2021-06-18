import context
from config import config
from dungeon.map_size_enum import MapSize
from network import communication
from settings import settings
from views.concrete.view_base import ViewBase
from views.concrete.view_room import ViewRoom
from views.input_enum import Input
from views.view_enum import Views


class ViewLobby(ViewBase):
    def __init__(self):
        super().__init__()
        self._notify_all_players_must_be_ready = False
        lobby_is_local = context.GAME.lobby.local_lobby
        self.options = [
            ["READY", Views.LOBBY, lambda: self.send_ready(), Input.SELECT],
            ["EXIT", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]
        # Host has a button to start a game
        if lobby_is_local:
            self.inputs = {
                "MAP SIZE": [1, ["SMALL", "MEDIUM", "LARGE"]]
            }
            self.options.insert(0, ["MAP SIZE", Views.LOBBY, lambda: None, Input.MULTI_TOGGLE])
            self.options.insert(0, ["START GAME", None, lambda: self.start_a_game(), Input.SELECT])

    def print_screen(self):
        self.print_text(context.GAME.lobby.address + ":" + str(context.GAME.lobby.port))
        participants = context.GAME.lobby.participants
        for player in participants:
            player_string = player.name + "[" + str(player.player_id) + "]"
            if player.ready:
                player_string += "[READY]"
            else:
                player_string += "[NOT READY]"

            print(player_string.center(settings["MAX_WIDTH"]))

        for i in range(config["MAX_PLAYERS"] - len(participants)):
            print("free".center(settings["MAX_WIDTH"]))
        print("")

        if self._notify_all_players_must_be_ready:
            print("ALL PLAYERS MUST BE READY TO START A GAME!".center(settings["MAX_WIDTH"]))
            self._notify_all_players_must_be_ready = False

        for option in self.options:
            to_print = option[0]
            value = self.get_input_of_option(option[0])
            if value is not None:
                to_print = to_print + ": " + str(value)
            if self.options.index(option) == self.selected:
                print((">" + to_print).center(settings["MAX_WIDTH"]))
            else:
                print(to_print.center(settings["MAX_WIDTH"]))

    def send_ready(self):
        lobby_is_local = context.GAME.lobby.local_lobby
        local_participant = context.GAME.lobby.get_local_participant()
        if lobby_is_local:
            local_participant.ready = not local_participant.ready

            # TODO It shouldn't be here...
            for client in context.GAME.sockets.values():
                communication.communicate(client, ["LOBBY_UPDATE", "ACTION:PLAYER_READY", "STATUS:" + str(local_participant.ready),
                                                   "PLAYER_ID:" + str(local_participant.player_id)])
        else:
            value = not local_participant.ready
            communication.communicate(context.GAME.host_socket, ["LOBBY_PLAYER_STATUS", "READY:" + str(value)])

    def start_a_game(self):
        for participant in context.GAME.lobby.participants:
            if not participant.ready:
                self._notify_all_players_must_be_ready = True
        if not self._notify_all_players_must_be_ready:
            # Generate map
            if self.inputs:
                if self.inputs["MAP SIZE"] == "SMALL":
                    context.GAME.generate_map(MapSize.SMALL)
                elif self.inputs["MAP SIZE"] == "MEDIUM":
                    context.GAME.generate_map(MapSize.MEDIUM)
                elif self.inputs["MAP SIZE"] == "LARGE":
                    context.GAME.generate_map(MapSize.LARGE)
                else:
                    context.GAME.generate_map(MapSize.MEDIUM)
            else:
                context.GAME.generate_map(MapSize.MEDIUM)

            context.GAME.begin_game_start_procedure()

        context.GAME.view_manager.refresh()
