from GameManager import Game
from PlayerAI import PlayerAI

if __name__ == '__main__':
    g = Game(
        size=4,
        target=2048
    )
    g.setPlayerAI(PlayerAI())
    g.Start()
