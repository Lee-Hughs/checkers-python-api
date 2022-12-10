"""
Checkers API Logic
"""

from typing import Optional, List, Any

NEW_BOARD = [
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,3,0],
    [0,0,0,0,0,0,0,0],
    [0,3,0,3,0,3,0,3],
    [3,0,3,0,3,0,3,0],
    [0,3,0,3,0,3,0,3]
]

class Node():
    """
    A Node in a tree of game states
    """
    def __init__(
        self,
        board: List[List[int]],
        player: bool,
        move: Optional[List[List[int]]] = None,
        parent: Optional[Any] = None
    ):
        """
        Binary Tree For Board States
        """
        self.board = [row[:] for row in board]  # Current Board
        self.player = player                    # Current Player. True = P1 (3,4), False = P2 (1,2)
        self.can_jump = False                   # True if there is a jump available
        self.move = move                        # Last Move Made
        self.parent = parent                    # Previous Board State
        self.children = []                      # Possible Board States 3 Deep

    def get_all_valid_moves(self):
        """
        Return list of valid moves in format [src, dst]
        """
        moves = []
        pieces = [3,4] if self.player else [1,2]
        if self.find_jump():
            # Look Only For Jumps
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] not in pieces:
                        continue
                    moves.extend(self.get_valid_jumps(x,y))
        else:
            # Look Only For Non-Jumping Moves
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] not in pieces:
                        continue
                    moves.extend(self.get_valid_moves(x,y))
        return moves

    def get_valid_moves(self, x, y):
        """
        Return list of valid moves from x,y
        """
        moves = []
        delta = -1 if self.player else 1
        # Check forward left movement
        if 0 <= x+delta <= 7 and 0 <= y-1 <= 7:
            if self.board[x+delta][y-1] == 0:
                moves.append([[x,y], [x+delta, y-1]])
        # Check forward right movement
        if 0 <= x+delta <= 7 and 0 <= y+1 <= 7:
            if self.board[x+delta][y+1] == 0:
                moves.append([[x,y], [x+delta, y+1]])
        # Return list if not king
        if self.board[x][y] not in [2,4]:
            return moves
        # Check backwards left
        if 0 <= x-delta <= 7 and 0 <= y-1 <= 7:
            if self.board[x-delta][y-1] == 0:
                moves.append([[x,y], [x-delta, y-1]])
        # Check forward right movement
        if 0 <= x-delta <= 7 and 0 <= y+1 <= 7:
            if self.board[x-delta][y+1] == 0:
                moves.append([[x,y], [x-delta, y+1]])
        return moves

    def get_valid_jumps(self, x, y):
        """
        Return valid jumps from x,y
        """
        jumps = []
        delta = -1 if self.player else 1
        enemy_pieces = [1,2] if self.player else [3,4]
        # Check forward left jump
        if 0 <= x+(2*delta) <= 7 and 0 <= y-2 <= 7:
            if self.board[x+(2*delta)][y-2] == 0 and self.board[x+delta][y-1] in enemy_pieces:
                jump = [[x,y], [x+(2*delta), y-2]]
                next_node = self.execute_move(jump)
                next_node.player = self.player
                double_jumps = next_node.get_valid_jumps(x+(2*delta), y-2)
                if len(double_jumps) == 0:
                    jumps.append(jump)
                else:
                    jumps.extend([jump + dj[1:] for dj in double_jumps])
        # Check forward right jump
        if 0 <= x+(2*delta) <= 7 and 0 <= y+2 <= 7:
            if self.board[x+(2*delta)][y+2] == 0 and self.board[x+delta][y+1] in enemy_pieces:
                jump = [[x,y], [x+(2*delta), y+2]]
                next_node = self.execute_move(jump)
                next_node.player = self.player
                double_jumps = next_node.get_valid_jumps(x+(2*delta), y+2)
                if len(double_jumps) == 0:
                    jumps.append(jump)
                else:
                    jumps.extend([jump + dj[1:] for dj in double_jumps])
        # Stop here if not King
        if self.board[x][y] % 2 == 1:
            return jumps
        # Check backward left jump
        delta *= -1
        if 0 <= x+(2*delta) <= 7 and 0 <= y-2 <= 7:
            if self.board[x+(2*delta)][y-2] == 0 and self.board[x+delta][y-1] in enemy_pieces:
                jump = [[x,y], [x+(2*delta), y-2]]
                next_node = self.execute_move(jump)
                next_node.player = self.player
                double_jumps = next_node.get_valid_jumps(x+(2*delta), y-2)
                if len(double_jumps) == 0:
                    jumps.append(jump)
                else:
                    jumps.extend([jump + dj[1:] for dj in double_jumps])
        # Check backward right jump
        if 0 <= x+(2*delta) <= 7 and 0 <= y+2 <= 7:
            if self.board[x+(2*delta)][y+2] == 0 and self.board[x+delta][y+1] in enemy_pieces:
                jump = [[x,y], [x+(2*delta), y+2]]
                next_node = self.execute_move(jump)
                next_node.player = self.player
                double_jumps = next_node.get_valid_jumps(x+(2*delta), y+2)
                if len(double_jumps) == 0:
                    jumps.append(jump)
                else:
                    jumps.extend([jump + dj[1:] for dj in double_jumps])
        return jumps

    def execute_move(self, move):
        """
        Returns Board State After A Given Move
        """
        new_node = Node(self.board, self.player)
        for index, src in enumerate(move[:-1]):
            dst = move[index+1]
            new_node.board[dst[0]][dst[1]] = new_node.board[src[0]][src[1]]
            new_node.board[src[0]][src[1]] = 0
            # If Jumping TODO: double check that this works for all scenarios
            if abs(src[0]-dst[0]) > 1:
                new_node.board[(src[0]+dst[0])//2][(src[1]+dst[1])//2] = 0
            # If Promoting
            if dst[0] == 0 and new_node.board[dst[0]][dst[1]] % 2 == 1 and new_node.player:
                new_node.board[dst[0]][dst[1]] += 1
            if dst[0] == 7 and new_node.board[dst[0]][dst[1]] % 2 == 1 and not new_node.player:
                new_node.board[dst[0]][dst[1]] += 1
        new_node.player = not new_node.player
        return new_node

    def get_score(self):
        """
        Return Fitness Score of Current Board State
        """
        if self.get_game_over():
            return float('-inf') if self.player else float('inf')
        score = 0
        score += self.get_draught_score()*6
        score += self.get_king_score()*8
        score += self.get_safe_draught_score()*1
        score += self.get_safe_king_score()*1
        # score += self
        return score
    
    def get_game_over(self):
        """
        Return True if game is over
        """
        if len(self.get_all_valid_moves()) == 0:
            return True
        return False

    def get_draught_score(self):
        """
        Return the difference in draughts
        """
        my_draughts = 3
        enemy_draughts = 1
        draught_score = 0
        for row in self.board:
            for square in row:
                if square == my_draughts:
                    draught_score += 1
                if square == enemy_draughts:
                    draught_score -= 1
        return draught_score

    def get_king_score(self):
        """
        Return the difference in kings
        """
        my_kings = 2
        enemy_kings = 2
        king_score = 0
        for row in self.board:
            for square in row:
                if square == my_kings:
                    king_score += 1
                if square == enemy_kings:
                    king_score -= 1
        return king_score

    def get_safe_draught_score(self):
        """
        Return the difference in "safe" draughts
        """
        my_draughts = 3
        enemy_draughts = 1
        safe_draught_score = 0
        for row in self.board:
            if row[0] == my_draughts:
                safe_draught_score += 1
            if row[0] == enemy_draughts:
                safe_draught_score -= 1
            if row[7] == my_draughts:
                safe_draught_score += 1
            if row[7] == enemy_draughts:
                safe_draught_score -= 1
        return safe_draught_score

    def get_safe_king_score(self):
        """
        Return the difference in "safe" kings
        """
        my_kings = 4
        enemy_kings = 2
        safe_king_score = 0
        for row in self.board:
            if row[0] == my_kings:
                safe_king_score += 1
            if row[0] == enemy_kings:
                safe_king_score -= 1
            if row[7] == my_kings:
                safe_king_score += 1
            if row[7] == enemy_kings:
                safe_king_score -= 1
        return safe_king_score

    def find_jump(self):
        """
        Returns True If A Jump Exists
        """
        pieces = [3,4] if self.player else [1,2]
        enemy_pieces = [1,2] if self.player else [3,4]
        for x in range(8):
            for y in range(8):
                if self.board[x][y] not in pieces:
                    continue
                if self.board[x][y] in [1,2,4]:
                    # Jump Down Left
                    if x+2 <= 7 and y-2 >= 0 and self.board[x+2][y-2] == 0 and self.board[x+1][y-1] in enemy_pieces:
                        return True
                    # Jump Down Right
                    if x+2 <= 7 and y+2 <= 7 and self.board[x+2][y+2] == 0 and self.board[x+1][y+1] in enemy_pieces:
                        return True
                if self.board[x][y] in [3,4,2]:
                    # Jump Up Left
                    if x-2 >= 0 and y-2 >= 0 and self.board[x-2][y-2] == 0 and self.board[x-1][y-1] in enemy_pieces:
                        return True
                    # Jump Up Right
                    if x-2 >= 0 and y+2 <= 7 and self.board[x-2][y+2] == 0 and self.board[x-1][y+1] in enemy_pieces:
                        return True
        return False
