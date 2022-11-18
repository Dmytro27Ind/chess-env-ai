from gym.envs.registration import register
from gym_chess.envs.game.ChessGame import *

register(
    id='chess-v0',
    entry_point='gym_chess.envs:ChessEnv',
)