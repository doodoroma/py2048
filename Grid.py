from copy import deepcopy

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = (
    (-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)


class Grid:
    """Representing the Board of the game
    """

    def __init__(self, size=4):
        """Grid constructor

        Keyword Arguments:
            size {int} -- Size of the board (size*size) (default: {4})
        """
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def __repr__(self):
        return '\n'.join([
            ','.join([
                f'{cell:4d}' for cell in line
            ]) for line in self.map
        ])

    def clone(self):
        """Make a deep copy of the board

        Returns:
            Grid -- Copy of the board
        """
        gridCopy = Grid()
        gridCopy.map = deepcopy(self.map)
        gridCopy.size = self.size

        return gridCopy

    def insertTile(self, pos, value):
        """Insert a new tile to a given position

        Arguments:
            pos {tuple} -- (x, y) position of the new value
            value {number} -- non-zero value of the tile
        """
        self.setCellValue(pos, value)

    def setCellValue(self, pos, value):
        """Change value of a tile at the given position

        Arguments:
            pos {tuple} -- (x, y) position of the new value
            value {number} -- non-zero value of the tile
        """
        self.map[pos[0]][pos[1]] = value

    def getAvailableCells(self):
        """Get all empty (with value 0) cells on the board

        Returns:
            list -- list of (x, y) tuples
        """
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x, y))

        return cells

    def getMaxTile(self):
        """Get maximum vaue on the board. Used to check the winning status

        Returns:
            number -- max tile value on board
        """
        maxTile = 0

        for x in range(self.size):
            for y in range(self.size):
                maxTile = max(maxTile, self.map[x][y])

        return maxTile

    def canInsert(self, pos):
        """Checks if the tile is empty or not at the given position

        Arguments:
            pos {tuple} -- (x, y) position

        Returns:
            bool -- if value is 0
        """
        return self._getCellValue(pos) == 0

    def move(self, direction):
        """Execute a move to a given direction
        All non-zero tile goes toward the direction until other non-zero cell
        becomes the neighbour.
        If the neighbour cell has the same value, the cells merge
        (values added)

        Arguments:
            dir {number} -- index of the movement from [UP, DOWN, LEFT, RIGHT]

        Returns:
            bool -- The movement was successful or not. If there was no change
            between the new and the old board, it returns `False`
        """
        direction = int(direction)

        if direction == UP:
            return self._moveUD(False)
        if direction == DOWN:
            return self._moveUD(True)
        if direction == LEFT:
            return self._moveLR(False)
        if direction == RIGHT:
            return self._moveLR(True)

    def _moveUD(self, down):
        r = range(self.size - 1, -1, -1) if down else range(self.size)

        moved = False

        for j in range(self.size):
            cells = []

            for i in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self._merge(cells)

            for i in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    def _moveLR(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)

        moved = False

        for i in range(self.size):
            cells = []

            for j in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self._merge(cells)

            for j in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    @staticmethod
    def _merge(cells):
        if len(cells) <= 1:
            return cells

        i = 0

        while i < len(cells) - 1:
            if cells[i] == cells[i+1]:
                cells[i] *= 2

                del cells[i+1]

            i += 1

    def canMove(self, dirs=vecIndex):
        """Check if the board can change into given directions

        Keyword Arguments:
            dirs {list} -- list of indices of directions (default: {vecIndex})

        Returns:
            bool -- If one of the direction can change the board, return `True`
        """
        # Init Moves to be Checked
        checkingMoves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):

                # If Current Cell is Filled
                if self.map[x][y]:

                    # Look Ajacent Cell Value
                    for i in checkingMoves:
                        move = directionVectors[i]

                        adjCellValue = self._getCellValue(
                            (x + move[0], y + move[1]))

                        # If Value is the Same or Adjacent Cell is Empty
                        if adjCellValue == self.map[x][y] or adjCellValue == 0:
                            return True

                # Else if Current Cell is Empty
                elif self.map[x][y] == 0:
                    return True

        return False

    def getAvailableMoves(self, dirs=vecIndex):
        """Filter directions towards which the board changes

        Keyword Arguments:
            dirs {list} -- list of indicies of directions (default: {vecIndex})

        Returns:
            list -- subset of `dirs` towards which the board changes
        """
        availableMoves = []

        for x in dirs:
            gridCopy = self.clone()

            if gridCopy.move(x):
                availableMoves.append(x)

        return availableMoves

    def _crossBound(self, pos):
        return (
            pos[0] < 0 or
            pos[0] >= self.size or
            pos[1] < 0 or
            pos[1] >= self.size
        )

    def _getCellValue(self, pos):
        if not self._crossBound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None
