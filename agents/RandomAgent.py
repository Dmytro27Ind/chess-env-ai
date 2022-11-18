import random

from gym_chess import *


class RandomAgent():
    """Táto trieda predstavuje agenta, ktorý robí náhodné šachové ťahy."""
    def make_move(self, game: ChessGame) -> list:
        """
        :param game: objekt ktorý predstavuje šachovú hru
        :return: vráti pohyb
        """
        return random.choice(game.get_available_moves())
