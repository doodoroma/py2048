class IPlayer:
    """Base class for py2048 player
    """

    def GetMove(self, grid):
        """Player shall decide the next move depending on the current state of the grid

        Arguments:
            grid {Grid} -- Copy of the grid
        """
        pass
