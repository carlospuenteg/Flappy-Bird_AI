# Flappy-Bird_AI
Flappy Bird game solved with [neat-python](https://neat-python.readthedocs.io/en/latest/), a Python module based on the [NEAT](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies) genetic algorithm

Based on [this](https://youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2) tutorial:
- [His repository](https://github.com/techwithtim/NEAT-Flappy-Bird)
- [NEAT explanation](https://youtu.be/OGHA-elMrxI)



## My additions to the game:
- Several constants can be changed:
  - Gap between both pipes
  - Distance between each two pipes
  - Maximum run time, maximum score and maximum generations after which the game stops
  - The FPS
  - The configuration (explained later)
  - The bird velocity
- Some display settings can be changed:
  - The window size
  - The caption
  - The fonts
  - The animation time of the bird's animation
- You can add a new [NEAT configuration](https://neat-python.readthedocs.io/en/latest/config_file.html) to the 'config' folder (with the name config1, config2,...)
