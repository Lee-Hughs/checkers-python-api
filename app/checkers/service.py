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
    # root.can_jump = root.find_jump()
    moves_list = root.get_all_valid_moves()
    print(moves_list)
    if len(moves_list) == 0:
        for row in board:
            print(row)
        return "Oops"
    if len(moves_list) == 1:
        return moves_list[0]
    moves_map = {
        index: mini_max(root.execute_move(move), 3, float('-inf'), float('inf'))
            for index, move in enumerate(moves_list)
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
    if depth == 0 or root.get_game_over():
        return root.get_score()
    root.children = [root.execute_move(move) for move in root.get_all_valid_moves()]
    if root.player:
        maxScore = float('-inf')
        for child in root.children:
            score = mini_max(child, depth-1, alpha, beta)
            maxScore = max(maxScore, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore
    minScore = float('inf')
    for child in root.children:
        score = mini_max(child, depth-1, alpha, beta)
        minScore = min(minScore, score)
        beta = min(beta, score)
        if beta <= alpha:
            break
    return minScore
