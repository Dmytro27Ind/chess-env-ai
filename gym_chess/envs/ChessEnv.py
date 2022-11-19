from multiprocessing import Pipe, Process

import gym
import numpy as np
from gym.spaces import Box
from tabulate import tabulate
from termcolor import colored

from gym_chess.envs.UI.ChessUI import make_chess_ui
from gym_chess.envs.space.ChessMoveSpace import ChessMoveSpace
from gym_chess.envs.game.ChessGame import *

CLOSE_ENV = -1

# Odmeny, ktoré sa vrátia agentovi
_rewards = {
    'playing': 0,
    'draw': 0,
    'win': 100
}


class ChessEnv(gym.Env):
    """
    Táto trieda predstavuje prostredie pre hranie šachu. Od agentov sa očakáva,
    že budú robiť pohyby, ktoré sú v súlade s pravidlami, inak sa vygeneruje chyba
    ValueError. Rozhodli sme sa dať agentom odmeny iba za výhru +100 alebo remízu
    +0 v šachovej partii a počas hry sa odmena bude rovnať +0.

    Hlavné metódy, ktoré musia používatelia tejto triedy poznať, sú:

        reset - resetovať stav prostredia na počiatočný.
        step - pomocou tejto metódy je možné urobiť pohyb v prostredí.
        render - vykresľovanie prostredia.
        close - uzavretie prostredia.

    Rovnako ako nasledujúce atribúty, ktoré musíme poznať:

        game - objekt typu ChessGame, ktorý predstavuje šachovú hru.
        action_space - objekt typu ChessMoveSpace, ktorý predstavuje všetky
            možné ťahy pre aktuálny stav prostredia.
        observation - tento objekt predstavuje šachovnicu.
        count - počítadlo ťahov v hre

    """
    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()
        self.proc = Process(target=make_chess_ui, args=(self.child_conn,))
        self.reset()

    def reset(self):
        self.game = ChessGame()
        self.action_space = ChessMoveSpace(self.game)
        self.observation_space = Box(low=np.array([0, 0]), high=np.array([1, 1]))   # Moc object for compiler
        self.observ_space = self.game.board
        self.count = 0
        return self.observ_space

    def step(self, action: list) -> [list, int, bool, int]:
        if self.game.make_move(action):
            self.count += 1
        else:
            raise ValueError

        if self.game.status == DRAW:
            return self.observ_space, _rewards['draw'], True, {'count': self.count, 'status': self.game.status}
        if self.game.status == WHITE_WIN or self.game.status == BLACK_WIN:
            return self.observ_space, _rewards['win'], True, {'count': self.count, 'status': self.game.status}

        return self.observ_space, _rewards['playing'], False, {'count': self.count, 'status': self.game.status}

    def close(self):
        self.parent_conn.send(CLOSE_ENV)

    def render(self, mode="human"):
        # vykreslenie epizódy v samostatnom procese pre GUI
        if mode == "human":
            if not self.proc.is_alive():
                self.proc.start()
            self.parent_conn.send({'board': self.game.board,
                                   'status': self.game.status,
                                   'white_takes': self.game.white_takes,
                                   'black_takes': self.game.black_takes,
                                   'white_score': self.game.delta_score_white})

        # jednoduchá vizualizácia epizódy v konzole
        elif mode == "ansi":
            # vytvorenie prázdnej tabuľky 8x8
            table = [[' ' for _ in range(8)] for _ in range(8)]

            for i in range(8):
                for j in range(8):
                    symbol = '⼀'
                    if self.game.board[i][j] == B_PAWN:
                        symbol = colored('♙', 'red')
                    elif self.game.board[i][j] == B_KNIGHT:
                        symbol = colored('♘', 'red')
                    elif self.game.board[i][j] == B_BISHOP:
                        symbol = colored('♗', 'red')
                    elif self.game.board[i][j] == B_ROOK:
                        symbol = colored('♖', 'red')
                    elif self.game.board[i][j] == B_QUEEN:
                        symbol = colored('♕', 'red')
                    elif self.game.board[i][j] == B_KING:
                        symbol = colored('♔', 'red')

                    elif self.game.board[i][j] == W_PAWN:
                        symbol = '♟'
                    elif self.game.board[i][j] == W_KNIGHT:
                        symbol = '♞'
                    elif self.game.board[i][j] == W_BISHOP:
                        symbol = '♝'
                    elif self.game.board[i][j] == W_ROOK:
                        symbol = '♜'
                    elif self.game.board[i][j] == W_QUEEN:
                        symbol = '♛'
                    elif self.game.board[i][j] == W_KING:
                        symbol = '♚'

                    table[i][j] = symbol
            print("move: " + str(self.count))
            print(tabulate(table))