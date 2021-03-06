import context
from config import config
from dungeon.map_size_enum import MapSize
from network import communication
from views.concrete.view_base import ViewBase
from views.input_enum import Input
from views.view_enum import Views


class ViewLobby(ViewBase):
    def __init__(self):
        super().__init__()
        # bool used to notify about ready status
        self._notify_all_players_must_be_ready = False

        # is local player the host?
        lobby_is_local = context.GAME.lobby.local_lobby

        self.options = [
            ["READY", Views.LOBBY, lambda: self._send_ready(), Input.SELECT],
            ["EXIT", Views.MENU, lambda: context.GAME.abandon_lobby(), Input.SELECT]
        ]

        # Host has a button to start a game
        if lobby_is_local:
            self.inputs = {
                "MAP SIZE": [1, ["SMALL", "MEDIUM", "LARGE"]]
            }
            self.options.insert(0, ["MAP SIZE", Views.LOBBY, lambda: None, Input.MULTI_TOGGLE])
            self.options.insert(0, ["START GAME", None, lambda: self._start_a_game(), Input.SELECT])

    def print_screen(self):
        self.print_multiline_text("\nListening on {address}:{port}\n"
                                  .format(address=context.GAME.lobby.address, port=str(context.GAME.lobby.port)))

        # Print slots
        self._print_participants()
        self._print_empty_slots()

        # All players must be ready...
        self._notify_ready()

        self._print_options()

    def _notify_ready(self):
        """
        Prints that everyone needs to be ready in order to start a game
        """
        if self._notify_all_players_must_be_ready:
            self.print_text("All players must be ready to start a game!")
            self._notify_all_players_must_be_ready = False

    def _print_empty_slots(self):
        """
        Prints strings representing empty slots
        """
        empty_slots = config["MAX_PLAYERS"] - len(context.GAME.lobby.participants)
        for i in range(empty_slots):
            self.print_text("- EMPTY -")
        self.print_text("\n")

    def _print_participants(self):
        """
        Prints all players, their ids and their ready status
        :return:
        """
        participants = context.GAME.lobby.participants
        for player in participants:
            status = "READY" if player.ready else "NOT READY"
            player_string = "{name}[{id}][{status}]".format(name=player.name, id=str(player.player_id), status=status)

            self.print_text(player_string)

    def _send_ready(self):
        """
        Toggles ready status and sends this information to host or other users
        """
        lobby_is_local = context.GAME.lobby.local_lobby
        local_participant = context.GAME.lobby.get_local_participant()
        if lobby_is_local:
            local_participant.ready = not local_participant.ready

            for client in context.GAME.sockets.values():
                communication.communicate(client, ["LOBBY_UPDATE", "ACTION:PLAYER_READY",
                                                   "STATUS:" + str(local_participant.ready),
                                                   "PLAYER_ID:" + str(local_participant.player_id)])
        else:
            value = not local_participant.ready
            communication.communicate(context.GAME.host_socket, ["LOBBY_PLAYER_STATUS", "READY:" + str(value)])

    def _start_a_game(self):
        """
        Try to start a game - check if all players are ready, generate map and start the game
        """
        for participant in context.GAME.lobby.participants:
            if not participant.ready:
                self._notify_all_players_must_be_ready = True

        if not self._notify_all_players_must_be_ready:
            # Generate map
            map_size = MapSize.MEDIUM
            if self.inputs:
                if self.get_input_of_option("MAP SIZE") == "SMALL":
                    map_size = MapSize.SMALL
                elif self.get_input_of_option("MAP SIZE") == "LARGE":
                    map_size = MapSize.LARGE
            context.GAME.generate_map(map_size)

            context.GAME.begin_game_start_procedure()

        context.GAME.view_manager.refresh()
