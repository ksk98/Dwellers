import context
from config import config
from dungeon.map_size_enum import MapSize
from network import communication
from settings import settings
from views.concrete.view_base import ViewBase
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
        self.print_multiline_text("\nListening on {address}:{port}\n"
                                  .format(address=context.GAME.lobby.address, port=str(context.GAME.lobby.port)))
        participants = self.print_participants()

        self.print_empty_slots(participants)

        self.notify_ready()

        self._print_options()

    def send_ready(self):
        """
        Toggles ready status and sends this information to host or other users
        """
        lobby_is_local = context.GAME.lobby.local_lobby
        local_participant = context.GAME.lobby.get_local_participant()
        if lobby_is_local:
            local_participant.ready = not local_participant.ready

            # TODO It shouldn't be here...
            for client in context.GAME.sockets.values():
                communication.communicate(client, ["LOBBY_UPDATE", "ACTION:PLAYER_READY",
                                                   "STATUS:" + str(local_participant.ready),
                                                   "PLAYER_ID:" + str(local_participant.player_id)])
        else:
            value = not local_participant.ready
            communication.communicate(context.GAME.host_socket, ["LOBBY_PLAYER_STATUS", "READY:" + str(value)])

    def start_a_game(self):
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

    def print_participants(self):
        participants = context.GAME.lobby.participants
        for player in participants:
            status = "READY" if player.ready else "NOT READY"
            player_string = "{name}[{id}][{status}]".format(name=player.name, id=str(player.player_id), status=status)

            self.print_text(player_string)
        return participants

    def print_empty_slots(self, participants):
        empty_slots = config["MAX_PLAYERS"] - len(participants)
        for i in range(empty_slots):
            self.print_text("- EMPTY -")
        self.print_text("\n")

    def notify_ready(self):
        if self._notify_all_players_must_be_ready:
            print("ALL PLAYERS MUST BE READY TO START A GAME!".center(settings["MAX_WIDTH"]))
            self._notify_all_players_must_be_ready = False
