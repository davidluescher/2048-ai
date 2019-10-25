from copy import deepcopy
from numpy import ndindex
from heuristicai import calculate_empty_tiles, calculate_board_score, execute_move
import heuristicai as heuristic


# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
move_args = [UP, DOWN, LEFT, RIGHT]
scores = [float(UP), float(DOWN), float(LEFT), float(RIGHT)]


def find_best_move(board):
    """
    find the best move for the next turn.
    """

    print("find_best_move called")
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    print("result set got returned with values: ", result)

    # Create new boards for each direction
    new_board_up = execute_move(UP, board)
    new_board_down = execute_move(DOWN, board)
    new_board_left = execute_move(LEFT, board)
    new_board_right = execute_move(RIGHT, board)

    # Check if the move in the direction UP, DOWN, LEFT or RIGHT is possible
    up_move_possible = heuristic.check_if_move_is_possible(board, new_board_up)
    down_move_possible = heuristic.check_if_move_is_possible(board, new_board_down)
    left_move_possible = heuristic.check_if_move_is_possible(board, new_board_left)
    right_move_possible = heuristic.check_if_move_is_possible(board, new_board_right)

    # Create a list of the best possible moves in a sequential order
    list_of_best_possible_moves = []


    """
    If the best move is not a valid move, choose the second best move. If a move is not a valid move, the score of that
    move will be set to -10 ^308, the smallest float representation possible in Python. 
    """

    if not down_move_possible:
        result[DOWN] = -float('inf')

    if not right_move_possible:
        result[RIGHT] = -float('inf')

    if not up_move_possible:
        result[UP] = -float('inf')

    if not left_move_possible:
        result[LEFT] = -float('inf')

    best_move = result.index(max(result))

    list_of_best_possible_moves.append(best_move)

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))
    print("The best move is: ", list_of_best_possible_moves[0])

    return list_of_best_possible_moves[0]


def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    print("score_toplevel_move called\n")
    print("Move: ", move, "\nBoard: \n", board)
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        print("The move", move, "is not valid.")
        return 0
    else:
        print("In else branch of score_toplevel_move")
        # Start the recursion
        if calculate_empty_tiles(newboard) <= 5:
            return expectimax(newboard, 4)
        else:
            return expectimax(newboard, 2)


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()


def expectimax(board, depth, turnHeuristics=False):
    print("Expectimax called")
    # When you reach the leaf calculate the board score
    if depth == 0 or (turnHeuristics and heuristic.game_over(board)):
        print("In depth==0 branch of expectimax with depth", depth)
        return calculate_board_score(board)

    # Take the valid move that maximises the score
    score = calculate_board_score(board)
    if turnHeuristics:
        print(" in turnHeuristics with depth", depth)
        for action in range(len(move_args)):
            print("The action is: ", action)
            child = execute_move(action, board)
            # Check if the move was a valid move
            if not board_equals(board, child):
                return max(score, expectimax(child, depth - 1, False))
            else:
                return score

    # When you don't reach the last depth, get all possible board states and calculate their scores dependence of the
    # probability this will occur. (recursively)
    else:
        print("In else branch of expectimax with depth", depth)
        score = 0
        probability = 1 / (calculate_empty_tiles(board)) if calculate_empty_tiles(board) > 0 else 0
        for i, j in ndindex(board.shape):
            current_score = 0
            if board[i, j] == 0:
                c1 = deepcopy(board)
                c1[i, j] = 2
                print("c1 is: \n")
                print(c1)
                score += 0.9 * expectimax(c1, depth - 1, True) * probability
                c2 = deepcopy(board)
                c2[i, j] = 4
                print("c2 is: \n")
                print(c2)
                score += 0.1 * expectimax(c2, depth - 1, True) * probability
        return score
