import os
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
        """
        Save all characters to file
        :return:
        """
        pickled_characters = jsonpickle.encode(saved_characters)
        f = open("save.txt", "w")
        f.write(pickled_characters)
        f.close()

    @staticmethod
    def load_from_file():
        """
        Loads all characters from file
        :return: True if characters are loaded successfully
        """
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
            return True

        except OSError:
            # no save file
            saved_characters.clear()
            return True

        except JSONDecodeError or AssertionError:
            # save file corrupted

            if f is not None:
                f.close()
            if os.path.isfile("save.txt"):
                os.rename("save.txt", "save.invalid.txt")

            saved_characters.clear()
            return False
