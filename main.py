import gym
import gym_chess
from agents.MinimaxAB import MinimaxAB
from agents.RandomAgent import RandomAgent
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    env = gym.make('chess-v0')
    white_agent = MinimaxAB()
    black_agent = RandomAgent()

    for i_episode in range(1000):
        print("Episode: " + str(i_episode))

        observation = env.reset()
        done = False
        while not done:
            env.render()
            # action = env.action_space.sample()
            if env.game.current_color == 'white':
                # action = black_agent.make_move(env.game)
                action = white_agent.make_move(env.game, 2)
            else:
                action = white_agent.make_move(env.game, 2)
                # action = black_agent.make_move(env.game)

            observation, reward, done, info = env.step(action)

            if action == [0] or action == [1]:
                print(" ______________________________ " + str(info['count']))

            # print("Move count: " + str(info['count']))

            if done:
                env.render()
                print("Game finished after " + str(info['count']) + " moves")
                print("Status: " + info['status'])
                print('\n')
                break

    env.close()