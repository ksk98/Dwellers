from logic.game import Game
import context


if __name__ == '__main__':
    context.GAME = Game()
    while context.GAME.running:
        context.GAME.tick()

    exit(0)
