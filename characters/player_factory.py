from json import JSONDecodeError

import jsonpickle

from characters.player import Player
from characters.saved_characters import saved_characters


class PlayerFactory:
    """
    Class created for saving / loading player character.
    """
    @staticmethod
    def load_player(name) -> Player:
        """
        Loads player character or creates new one
        :param name: name of the character
        :return: player object
        """
        if name in saved_characters:
            return saved_characters[name]
        else:
            return Player(name)

    @staticmethod
    def save_player(player: Player):
        """
        Save player object
        :param player: player to save
        """
        saved_characters[player.name] = player
        PlayerFactory.save_to_file()

    @staticmethod
    def delete(name):
        """
        Delete character.
        :param name: name of the character that will be removed.
        """
        if saved_characters.get(name):
            saved_characters.pop(name)
            PlayerFactory.save_to_file()

    @staticmethod
    def save_to_file():
        pickled_characters = jsonpickle.encode(saved_characters)
        f = open("save.txt", "w")
        f.write(pickled_characters)
        f.close()

    @staticmethod
    def load_from_file():
        # Clear saved characters
        saved_characters.clear()
        try:
            # Load from file
            f = open("save.txt", "r")
            unpickled_characters = jsonpickle.decode(f.read())
            assert isinstance(unpickled_characters, dict)

            # Add to dict
            saved_characters.update(unpickled_characters)
            f.close()

        except OSError:
            print("Warning! Save file not found!")
            saved_characters.clear()
            return

        except AssertionError:
            saved_characters.clear()
            return

        except JSONDecodeError:
            print("Warning! Save file corrupted!")
            saved_characters.clear()
            return
