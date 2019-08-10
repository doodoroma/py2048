from os import system, name

from Grid import Grid
from random import randint
import time

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)


class Game:
    """Class to handle workflow of the game and display
    status on the console"""

    def __init__(self, size=4, defaultInitialTiles=2, defaultProbability=0.9):
        """Game constructor

        Keyword Arguments:
            size {int} -- Size of the board (size * size) (default: {4})
            defaultInitialTiles {int} -- How many tiles to be initialized at
            the begining of the Game (default: {2})
            defaultProbability {float} -- Probablity of 2 or 4 values for
            every new tiles (default: {0.9})
        """
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles = defaultInitialTiles
        self.playerAI = None
        self.over = False

    def setPlayerAI(self, playerAI):
        """Set implementation of AI. You can define your own algorithm if you want

        Arguments:
            playerAI {IPlayer}
        """
        self.playerAI = playerAI

    def Start(self):
        """Start the whole game. You have to define the AI Player before
        starting the game"""
        for _ in range(self.initTiles):
            self._insertRandomTile()

        # Display the initial status of the board
        self._print_status()
        while not self._isGameOver():
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            # Ask AI for the next move
            move = self.playerAI.getMove(gridCopy)
            self.grid.move(move)
            self._print_status(move)

            # Add randomly a tile after each move
            cells = self.grid.getAvailableCells()
            new_tile_pos = cells[randint(0, len(cells) - 1)] if cells else None
            self.grid.setCellValue(new_tile_pos, self._getNewTileValue())
            self._print_status()

            time.sleep(0.2)

    @staticmethod
    def _clear():
        """Clear console
        """
        if name == 'nt':    # for windows
            system('cls')
        else:               # for mac and linux(here, os.name is 'posix')
            system('clear')

    def _print_status(self, move=None):
        self._clear()
        print('---------')
        print(self.grid)
        print('---------')
        if(self.grid.getMaxTile() >= 2048):
            print(f'Congrats! Score is {self.grid.getMaxTile()}')
        time.sleep(0.05)

    def _isGameOver(self):
        """Check if the board has a possibility to move or not

        Returns:
            bool -- true if no move possible
        """
        return not self.grid.canMove()

    def _getNewTileValue(self):
        """Get a new tile (usually 2 or 4 with given distribution)

        Returns:
            number -- value of the new tile
        """
        if randint(0, 99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    def _insertRandomTile(self):
        """Set randomly chosen empty cell a possible new tile value
        """
        tileValue = self._getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)
