import time
from GameManager import Game
from PlayerAI import PlayerAI


if __name__ == '__main__':
    g = Game()
    g.setPlayerAI(PlayerAI())
    g.Start()
