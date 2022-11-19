# Chess Environment
This is the Gym environment from OpenAI for AI training.

### [Link to bachelor's work PDF](https://drive.google.com/file/d/1EYY7fulLW65Wk9m5rKvaaauP8qrtMcn4/view?usp=sharing){:target="_blank"}

[![Watch the video](https://github.com/Dmytro27Ind/images/blob/main/chess-env-ai_video_screen.PNG)](https://www.youtube.com/watch?v=sfbLfX8UyGM&ab_channel=DmytroKagirov){:target="_blank"}

## Requirements
- You need to have Python 3.9 installed. Available at: https://www.python.org/downloads/
- pip must be installed to install all project dependencies. Available at: https://pypi.org/project/pip/

## Install
Steps to install the chess environment package:

1. `$ git clone https://github.com/Dmytro27Ind/chess-env-ai.git`

2. `$ cd chess-env-ai`

3. `$ pip install -e .`

## Example of using a chess environment

```python
import  gym
import  gym_chess

if  __name__  ==  "__main__":
	env  =  gym.make('chess-v0')

	for  i_episode  in  range(5):
		observation  =  env.reset ()
		done  =  False

		while  not  done:
			env.render()
			observation , reward , done , info  = \
			env.step(env. action_space .sample ())

			if  done:
				env.render()
				break

	env.close ()
```