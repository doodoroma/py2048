import time
from GameManager import Game
from PlayerAI import PlayerAI


def test_run():
    g = Game()
    g.setPlayerAI(PlayerAI())
    g.Start()
