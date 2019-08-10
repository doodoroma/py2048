"""
    Author: Adam Meszaros
    Date: 21-06-2017

"""
from IPlayer import IPlayer


class Node:
    """Node of the searching tree.
    Each node is a status of the Game (what move and what grid)
    Each Node represents a value (score). The goal is to define the Score to
    represent well how good the Node is for the Player.
    """
    parent = None
    grid = None
    score = 16
    move = -1

    def __init__(self, parent, grid):
        """Node constructor

        Arguments:
            parent {Node} -- Parent Node
            grid {Grid} -- Status of the grid for this Node
        """
        self.parent = parent
        self.grid = grid
        if parent is not None:
            self.move = parent.move


class PlayerAI(IPlayer):
    """My 2048 logic
    Implementation of an alpha-beta pruning
    """

    def __init__(self, search_depth=3):
        self.search_depth = search_depth

    def getMove(self, grid):
        """Get direction of the next move"""
        best = self._minmax(grid)
        while best.parent is not None and best.parent.parent is not None:
            best = best.parent

        if best.move < 0:
            return 0

        return best.move
        # moves = grid.getAvailableMoves()
        # return moves[randint(0, len(moves) - 1)] if moves else None

    @staticmethod
    def eval(grid):
        empty_cells_list = grid.getAvailableCells()

        # Heuristic 1: empty_cells -- More empty cell is better
        empty_cells = len(empty_cells_list)

        # Heuristic 2: place_sum -- Bigger values shall be on the border
        sum_tile = 0
        for r in grid.map:
            for e in r:
                sum_tile += e

        place_sum = 0
        for x in range(4):
            for y in range(4):
                place_sum += (
                    grid.map[x][y] * (
                        (1*int(x == 0 or x == 3 or y == 0 or y == 3)) +
                        (
                            1*int((x == 0 and y == 0) or (x == 0 and y == 3) or
                                  (x == 3 and y == 3) or (x == 3 and y == 0))
                        )

                    ))

        place_sum /= sum_tile

        # Heuristic 3: avgDiff -- big difference between neighbouring cells
        # is generally wrong
        avgDiff_list = []
        for x in range(4):
            for y in range(4):
                if x > 0 and grid.map[x - 1][y] > 0 and grid.map[x][y] > 0:
                    avgDiff_list.append(
                        max(grid.map[x - 1][y], grid.map[x][y]) /
                        min(grid.map[x - 1][y], grid.map[x][y])
                    )
                if x < 3 and grid.map[x + 1][y] > 0 and grid.map[x][y] > 0:
                    avgDiff_list.append(
                        max(grid.map[x + 1][y], grid.map[x][y]) /
                        min(grid.map[x + 1][y], grid.map[x][y])
                    )
                if y > 0 and grid.map[x][y - 1] > 0 and grid.map[x][y] > 0:
                    avgDiff_list.append(
                        max(grid.map[x][y - 1], grid.map[x][y]) /
                        min(grid.map[x][y - 1], grid.map[x][y])
                    )
                if y < 3 and grid.map[x][y + 1] > 0 and grid.map[x][y] > 0:
                    avgDiff_list.append(
                        max(grid.map[x][y + 1], grid.map[x][y]) /
                        min(grid.map[x][y + 1], grid.map[x][y])
                    )

        avgDiff = 1
        if len(avgDiff_list) > 1:
            avgDiff = sum(avgDiff_list) / len(avgDiff_list) - 1

        # Heuristic 4: monotic -- Monotic change allows merging
        # in the future. The goal is to avoid situation like [0 16 64 32]
        # It is better if it is like [0 16 32 64]
        row_monotic_inc = 0
        row_monotic_dec = 0
        row_monotic_eq = 0
        ncompare = 0
        row_monotic = 0
        for x in range(4):
            for y in range(3):
                if grid.map[x][y] != 0:
                    row_monotic_inc += int(grid.map[x][y] < grid.map[x][y + 1])
                    row_monotic_dec += int(grid.map[x][y] > grid.map[x][y + 1])
                    row_monotic_eq += int(grid.map[x][y] == grid.map[x][y + 1])
                    ncompare += 1
        if ncompare > 0:
            if row_monotic_inc > row_monotic_dec:
                row_monotic_inc += row_monotic_eq
            else:
                row_monotic_dec += row_monotic_eq
            row_monotic = abs(row_monotic_inc - row_monotic_dec) / ncompare

        col_monotic_inc = 0
        col_monotic_dec = 0
        col_monotic_eq = 0
        ncompare = 0
        col_monotic = 0
        for y in range(4):
            for x in range(3):
                if grid.map[x][y] != 0:
                    col_monotic_inc += int(grid.map[x][y] < grid.map[x + 1][y])
                    col_monotic_dec += int(grid.map[x][y] > grid.map[x + 1][y])
                    col_monotic_eq += int(grid.map[x][y] == grid.map[x + 1][y])
                    ncompare += 1
        if ncompare > 0:
            if col_monotic_inc > col_monotic_dec:
                col_monotic_inc += col_monotic_eq
            else:
                col_monotic_dec += col_monotic_eq
            col_monotic = abs(col_monotic_inc - col_monotic_dec) / ncompare

        monotic = (row_monotic + col_monotic) * 0.5

        # Heuristic 5: avg_value -- Monotic change allows merging
        avg_value = sum_tile / (
            (grid.size * grid.size) - len(empty_cells_list)
        )

        # return the combination of the heuristics with scaling
        return (
            empty_cells / 12 +
            place_sum * 5 -
            avgDiff / 32 +
            monotic * 3 +
            avg_value / 32
        )

    def _minmax(self, grid):
        return self._maximize(
            Node(None, grid),
            -99999,
            99999,
            self.search_depth
        )

    def _minimize(self, node, alfa, beta, depth):
        cells = node.grid.getAvailableCells()
        if depth <= 0 or node.score <= 0 or len(cells) == 0:
            node.score = self.eval(node.grid)
            return node

        minNode = Node(node, None)
        minNode.score = 99999

        for c in cells:
            child = Node(node, node.grid.clone())
            child.grid.insertTile(c, 2)
            child = self._maximize(child, alfa, beta, depth - 1)
            if child.score < minNode.score:
                minNode = child
            if minNode.score <= alfa:
                break

            if minNode.score < beta:
                beta = minNode.score

        return minNode

    def _maximize(self, node, alfa, beta, depth):
        if depth <= 0 or node.score <= 0:
            node.score = self.eval(node.grid)
            return node

        maxNode = Node(node, None)
        maxNode.score = -99999
        moves = node.grid.getAvailableMoves()
        for m in moves:
            node.move = m
            child = Node(node, node.grid.clone())
            child.grid.move(m)
            child.move = m
            child = self._minimize(child, alfa, beta, depth - 1)
            if child.score > maxNode.score:
                maxNode = child

            if maxNode.score >= beta:
                break

            if maxNode.score > alfa:
                alfa = maxNode.score

        return maxNode
