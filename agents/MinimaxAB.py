import math
import random

from anytree import Node

from gym_chess import *


class Value:
    """ Táto trieda predstavuje hodnotu pre uzol v strome vyhľadávania
     ťahov šachovej hry.

    move - je ťah v šachovej hre.
    value - je hodnota na šachovnici po tomto ťahu.
    """
    def __init__(self, move, value):
        self.move = move
        self.value = value


class MNode(Node):
    """Zdedí triedu Node z balíka a prepíše metódy
     na porovnávanie hodnôt uzlov."""
    def __lt__(self, other):
        return self.name.value < other.name.value

    def __le__(self, other):
        return self.name.value <= other.name.value

    def __eq__(self, other):
        return self.name.value == other.name.value

    def __ne__(self, other):
        return self.name.value != other.name.value

    def __gt__(self, other):
        return self.name.value > other.name.value

    def __ge__(self, other):
        return self.name.value >= other.name.value

    def __lt__(self, other: float):
        return self.name.value < other

    def __le__(self, other: float):
        return self.name.value <= other

    def __eq__(self, other: float):
        return self.name.value == other

    def __ne__(self, other: float):
        return self.name.value != other

    def __gt__(self, other: float):
        return self.name.value > other

    def __ge__(self, other: float):
        return self.name.value >= other


class MinimaxAB:
    """Táto trieda je agent, ktorý používa metódu minimax s orezaním podľa
    Alpha–beta na nájdenie najlepšieho ťahu v šachovej hre do určitej hĺbky.
    """

    def make_move(self, game: ChessGame, deep: int) -> list:
        """

        :param game: objekt ktorý predstavuje šachovú hru. Je to potrebné, aby
                     agent poznal aktuálny stav na šachovnici a vedel triediť ťahy,
                     aby našiel ten najlepší.
        :return: Vráti najlepší ťah
        """
        white = True if game.current_color == 'white' else False
        vgame = copy.deepcopy(game)
        node = self.__alpha_beta(None, None, deep, -math.inf, math.inf, white, vgame)
        return node.path[1].name.move

    def __alpha_beta(self, node, move, depth, alpha, beta, maximizing, game: ChessGame):
        """ Minimax algoritmus s alfa-beta prerezávaním.
        :param node: uzol v strome vyhľadávania šachových ťahov
        :param move: šachový ťah
        :param depth: hĺbka hľadania najlepšieho šachového ťahu
        :param alpha: spočiatku -inf
        :param beta: spočiatku inf
        :param maximizing: biely alebo čierny hráč
        :param game: objekt hry
        :return: Vráti uzol s najlepším ťahom
        """
        if depth == 0:
            return node

        if node is None:
            node = MNode(Value(move, None))
            node.children = []

        moves = game.get_available_moves()
        random.shuffle(moves)
        if not moves:
            node.name.value = self.board_value(game.board)

        if maximizing:
            value = -math.inf
            if not moves:
                return node
            for child_move in moves:
                vgame = copy.deepcopy(game)
                vgame.make_move(child_move)
                child = MNode(Value(child_move, self.board_value(vgame.board)))
                child.children = []
                node.children += (child,)
                eval = self.__alpha_beta(child, child_move, depth - 1, alpha, beta, False, vgame)

                value = max(value, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            if not moves:
                return node
            for child_move in moves:
                vgame = copy.deepcopy(game)
                vgame.make_move(child_move)
                child = MNode(Value(child_move, self.board_value(vgame.board)))
                child.children = []
                node.children += (child,)
                eval = self.__alpha_beta(child, child_move, depth - 1, alpha, beta, True, vgame)

                value = min(value, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break
            return value

    def board_value(self, board) -> int:
        """
        Táto metóda vyhodnotí aktuálny stav šachovnice a vráti výsledok
        :param board: šachovnica
        :return: vráti výsledok
        """
        value = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == W_PAWN:
                    value += PAWN_COST
                elif board[i][j] == W_BISHOP:
                    value += BISHOP_COST
                elif board[i][j] == W_KNIGHT:
                    value += KNIGHT_COST
                elif board[i][j] == W_ROOK:
                    value += ROOK_COST
                elif board[i][j] == W_QUEEN:
                    value += QUEEN_COST

                elif board[i][j] == B_PAWN:
                    value -= PAWN_COST
                elif board[i][j] == B_BISHOP:
                    value -= BISHOP_COST
                elif board[i][j] == B_KNIGHT:
                    value -= KNIGHT_COST
                elif board[i][j] == B_ROOK:
                    value -= ROOK_COST
                elif board[i][j] == B_QUEEN:
                    value -= QUEEN_COST
        return value