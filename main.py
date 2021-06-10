from logic.game import Game
from views.concrete.view_menu import ViewMenu
import context
import socket


if __name__ == '__main__':
    context.MENU = ViewMenu()
    context.GAME = Game()

    try:
        while context.GAME.running:
            context.GAME.tick()
    except socket.error as e:
        print(e)

    exit(0)
