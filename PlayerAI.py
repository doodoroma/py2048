"""
    AI Course Project 4 module

    Author: Adam Meszaros
    Date: 21-06-2017

"""
from random import randint
from IPlayer import IPlayer
import math
import queue
import statistics

class Node:
    parent = None
    grid = None
    score = 16
    move = -1
    def __init__(self, parent, grid):
        self.parent = parent
        self.grid = grid
        if parent != None:
            self.move = parent.move

class PlayerAI(IPlayer):
    """My 2048 logic"""

    def getMove(self, grid):
        """Get direction of the next move"""
        best = self.minmax(grid)
        while best.parent != None and best.parent.parent != None:
            best = best.parent

        if best.move < 0:
            return 0

        return best.move
        # moves = grid.getAvailableMoves()
        # return moves[randint(0, len(moves) - 1)] if moves else None

    def eval(self, grid):
        empty_cells_list = grid.getAvailableCells()
        # Heuristic 1: More empty cell is better
        empty_cells = len(empty_cells_list)
        empty_cells /= 12

        # Bigger values shall be on the border
        sum_tile = 0
        for r in grid.map:
            for e in r:
                sum_tile += e

        avgValue = sum_tile / (16 - len(empty_cells_list)) / grid.getMaxTile()

        place_sum = 0
        for x in range(4):
            for y in range(4):
                place_sum += grid.map[x][y] \
                    * ((1*int(x == 0 or x == 3 or y == 0 or y == 3)) \
                    + (1*int((x == 0 and y == 0) or (x == 0 and y == 3) or (x == 3 and y == 3) or (x == 3 and y == 0))))

        place_sum /= sum_tile

        avgDiff_list = []
        for x in range(4):
            for y in range(4):
                if x > 0 and grid.map[x - 1][y] > 0 and  grid.map[x][y] > 0:
                    avgDiff_list.append(max(grid.map[x - 1][y], grid.map[x][y]) / min(grid.map[x - 1][y], grid.map[x][y]))
                if x < 3 and grid.map[x + 1][y] > 0 and  grid.map[x][y] > 0:
                    avgDiff_list.append(max(grid.map[x + 1][y], grid.map[x][y]) / min(grid.map[x + 1][y], grid.map[x][y]))
                if y > 0 and grid.map[x][y - 1] > 0 and  grid.map[x][y] > 0:
                    avgDiff_list.append(max(grid.map[x][y - 1], grid.map[x][y]) / min(grid.map[x][y - 1], grid.map[x][y]))
                if y < 3 and grid.map[x][y + 1] > 0 and  grid.map[x][y] > 0:
                    avgDiff_list.append(max(grid.map[x][y + 1], grid.map[x][y]) / min(grid.map[x][y + 1], grid.map[x][y]))
        
        # print(avgDiff_list)
        avgDiff = 1
        if len(avgDiff_list) > 0:
            avgDiff = sum(avgDiff_list)/len(avgDiff_list) - 1

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


        avg_value = sum_tile / (16 - len(empty_cells_list))
        # print('empty_cells=' + str(empty_cells))
        # print('place_sum=' + str(place_sum))
        # print('monotic=' + str(monotic))
        # print('avgDiff=' + str(avgDiff))
        # print('avgValue=' + str(avgValue))
        # print('sum_tile=' + str(avg_value))
        return empty_cells + place_sum * 5 + monotic * 3 + avg_value / 32 - avgDiff / 32

    def minmax(self, grid):
        return self.maximize(Node(None, grid), -99999, 99999, 3)
        
    def minimize(self, node, alfa, beta, depth):
        cells = node.grid.getAvailableCells()
        if depth <= 0 or node.score <= 0 or len(cells) == 0:
            node.score = self.eval(node.grid)
            return node;

        minNode = Node(node, None);
        minNode.score = 99999
        

        for c in cells:
            child = Node(node, node.grid.clone())
            child.grid.insertTile(c, 2)
            child = self.maximize(child, alfa, beta, depth - 1)
            if child.score < minNode.score:
                minNode = child
            if minNode.score <= alfa:
                break;
            
            if minNode.score < beta:
                beta = minNode.score
        
        return minNode

    def maximize(self, node, alfa, beta, depth):
        if depth <= 0 or node.score <= 0:
            node.score = self.eval(node.grid)
            return node;

        maxNode = Node(node, None);
        maxNode.score = -99999
        moves = node.grid.getAvailableMoves()
        for m in moves:
            node.move = m
            child = Node(node, node.grid.clone())
            child.grid.move(m)
            child.move = m
            child = self.minimize(child, alfa, beta, depth - 1)
            if child.score > maxNode.score:
                maxNode = child

            if maxNode.score >= beta:
                break

            if maxNode.score > alfa:
                alfa = maxNode.score

        return maxNode
