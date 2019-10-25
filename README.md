# 2048-ai
AI for the [2048 game](http://gabrielecirulli.github.io/2048/). This solution uses *expectimax optimization*. Heuristics used include bonuses for empty squares, bonuses for adjacent tiles with the same value and bonuses for tiles that match a snake pattern on the board. 
This solution was developed as part of coursework Artificial Intelligence 1 at [Zurich University of Applied Sciences](https://www.zhaw.ch/en/university/) and is far from being an ideal solution. However, it reached the 2048 tile in the vast majority of the test runs (sample size > 20) and the average board score is about 30'000. 

For more information about the expectimax algorithm and useful heuristics check this [StackOverflow answer](https://stackoverflow.com/a/22498940/1204143).

## Running the browser-control version with Chrome

Enable Chrome remote debugging by starting it with the `remote-debugging-port` command-line switch (e.g. `google-chrome --remote-debugging-port=9222`).

Open up the [2048 game](http://gabrielecirulli.github.io/2048/), then run `2048.py -b chrome` via the command line and watch the game!
