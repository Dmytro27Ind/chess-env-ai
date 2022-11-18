import random

from gym import Space


class ChessMoveSpace(Space):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def sample(self):
        """
        :return: Táto metóda vráti náhodný ťah zo všetkých možných ťahov.
        """
        moves = self.game.get_available_moves()
        if not moves:
            return []
        return random.choice(moves)

    def contains(self, move) -> bool:
        """
        :param move: - ťah
        :return: Táto metóda vráti \verb|True|, ak je ťah \verb|move|, ktorý metóde odovzdávame, je v možných ťahoch.
        """
        if move in self.game.get_available_moves():
            return True
        else:
            return False

    def __contains__(self, item):
        return self.contains(item)