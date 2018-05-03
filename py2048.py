import argparse
import math
import PlayerAI
import Grid

move = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

if __name__ == "__main__":
    size = 4
    example = [[0] * size for i in range(size)]
    example[0][0] = 2
    example[0][2] = 2

    example = [
        2, 2, 0, 0, 
        0, 0, 0, 0, 
        0, 0, 0, 0, 
        0, 0, 0, 0
    ]

    parser = argparse.ArgumentParser(description='AI for the next 2048 move')
    parser.add_argument('--board', nargs="*", type=int, metavar="X X", default=example)
    args = parser.parse_args()

    size = math.sqrt(len(args.board))
    assert size.is_integer(), "Board size is not square"

    size = int(size)

    board = [args.board[x*4:(x*4+4)] for x in range(size)]

    Player = PlayerAI.PlayerAI()
    print(move[Player.getMove(Grid.Grid(size, board))])