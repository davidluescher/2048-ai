import sys
import game
from numpy import zeros, hstack, ndindex


# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
scores = [float(UP), float(DOWN), float(LEFT), float(RIGHT)]
move_args = [UP, DOWN, LEFT, RIGHT]

def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, new_board):
    """
    Check if two boards are equal
    """
    return (new_board == board).all()


def check_if_move_is_possible(board, new_board):
    """
    Check if the next move is an valid move
    :param board: current board
    :param new_board: board after the next move
    :return: True if boards aren't equal.  False if the boards equal
    """
    if board_equals(board, new_board):
        return False
    else:
        return True


def score_adjacent_tiles(board):
    """
    Calculate the weighted score for adjacent tiles.
    :param board:
    :return:
    """
    return (score_count_neighbor(board) + score_mean_neighbor(board)) / 2


def score_snake(board, base_value=0.25):
    """
    Calculate the score for the snake pattern. Higher scores will be returned for tiles that match the snake pattern
    on a board.
    """
    score = 0
    rewardArray = [base_value ** i for i in range(16)]
    for i in range(2):
        boardArray = hstack((board[0], board[1][::-1], board[2], board[3][::-1]))
        score = max(score, (rewardArray * boardArray).sum())
        score = max(score, (rewardArray[::-1] * boardArray).sum())
        boardArray = hstack((board[0][::-1], board[1], board[2][::-1], board[3]))
        score = max(score, (rewardArray * boardArray).sum())
        score = max(score, (rewardArray[::-1] * boardArray).sum())
        board = board.T
    return score


def score_mean_neighbor(newBoard):
    """
    Calculate the mean(average) of  tiles with the same values that are adjacent in a row/column.
    """
    horizontal_sum, count_horizontal = check_neighbor(newBoard)
    vertical_sum, count_vertical = check_neighbor(newBoard.T)
    if count_horizontal == 0 or count_vertical == 0:
        return 0
    return horizontal_sum / count_horizontal + vertical_sum / count_vertical


def check_neighbor(board):
    """
    Returns the sum and total number (count) of tiles with the same values that are adjacent in a row/column.
    """
    count = 0
    sum = 0
    for row in board:
        previous = -1
        for tile in row:
            if previous == tile:
                sum += tile
                count += 1
            previous = tile
    return sum, count


def score_count_neighbor(board):
    _, horizontal_count = check_neighbor(board)
    _, vertical_count = check_neighbor(board.T)
    return horizontal_count + vertical_count


def calculate_empty_tiles(board):
    empty_tiles = 0
    for x, y in ndindex(board.shape):
        if board[x, y] == 0:
            empty_tiles += 1
    return empty_tiles


def game_over(board):
    """
    Check if the game state is game over
    :param board:
    :return: True, if the game is over
    """
    for i in range(len(move_args)):
        print("Game Over called. i is: ", i)
        new_board = execute_move(i, board)
        if not board_equals(board, new_board):
            return False
    return True


def calculate_board_score(board):
    neighbor_score = score_adjacent_tiles(board)
    snake_score = score_snake(board)
    min_score = calculate_empty_tiles(board)
    result = min_score + snake_score + neighbor_score
    # Log statements for debugging
    print("snake_score is: ", snake_score)
    print("min_score is: ", min_score)
    print("neighbor_score is: ", neighbor_score)
    print("The board score is ", result)

    return result


