import context
from logic.game import Game

if __name__ == '__main__':
    context.GAME = Game()
    while context.GAME.running:
        context.GAME.tick()

    exit(0)
