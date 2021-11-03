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
            ch = saved_characters[name]
            return jsonpickle.decode(ch)
        else:
            return Player(name)

    @staticmethod
    def save_player(player: Player):
        """
        Save player object
        :param player: player to save
        """
        saved_characters[player.name] = jsonpickle.encode(player)

    @staticmethod
    def delete(name):
        """
        Delete character.
        :param name: name of the character that will be removed.
        """
        if saved_characters.get(name):
            saved_characters.pop(name)
