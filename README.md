# Rock Paper Scissors AI

### How to run the game
For trying the game you should create a file, ```runner.py``` for example, on src folder and copy the following code:

```
from main import Game

game = Game()
game.train(100000, lr=0.3, gamma=0.8)
game.play()
```
