from logic.game import Game
from views.concrete.view_menu import ViewMenu
import context
import socket


if __name__ == '__main__':
    context.MENU = ViewMenu()
    context.GAME = Game()

    try:
        context.GAME.view_manager.get_current().refresh_view()
        while context.GAME.running:
            context.GAME.tick()
    except socket.error as e:
        pass

    exit(0)
