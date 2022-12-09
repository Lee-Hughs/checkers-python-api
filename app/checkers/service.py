"""
Checkers endpoint services
"""

from typing import List
from app.checkers.node import Node

def get_best_move(board: List[List[int]]):
    """
    Get best move given a board state
    """
    root = Node(board=board, player=False)
    root.can_jump = root.find_jump()
    moves_list = root.get_all_valid_moves()
    print(moves_list)
    if len(moves_list) == 0:
        print("Error: No moves avilable")
        print("Debug:")
        for row in board:
            print(row)
        return
    # moves_map = {index: root.execute_move(move).get_score() for index, move in enumerate(moves_list)}
    moves_map = {
        index: mini_max(root.execute_move(move), 2, float('-inf'), float('inf')) for index, move in enumerate(moves_list)
    }
    print(moves_list)
    print(moves_map)
    best_move = min(moves_map, key=moves_map.get)
    print("Best move: ", best_move)
    return moves_list[best_move]

def mini_max(root: Node, depth: int, alpha: int, beta: int):
    """
    MiniMax algorithm with alpha beta pruning
    """
    print("Begin mini max depth: ", depth)
    if depth == 0 or root.get_game_over():
        return root.get_score()
    root.children = [root.execute_move(move) for move in root.get_all_valid_moves()]
    print("Length of children at depth: ", depth)
    print(len(root.children))
    if root.player:
        maxScore = float('-inf')
        print("Entering player loop")
        for child in root.children:
            print("About to call minimax again")
            score = mini_max(child, depth-1, alpha, beta)
            maxScore = max(maxScore, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = float('inf')
        print("Entering not player loop")
        for child in root.children:
            print("About to call minimax again")
            score = mini_max(child, depth-1, alpha, beta)
            minScore = min(minScore, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore