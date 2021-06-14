from logic.game import Game
import context
import socket


if __name__ == '__main__':
    context.GAME = Game()

    try:
        while context.GAME.running:
            context.GAME.tick()
    except socket.error as e:
        print(e)

    exit(0)
