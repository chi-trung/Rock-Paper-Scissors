"""
Logic và rules của game
"""
from enum import Enum


class Move(Enum):
    """Định nghĩa các nước đi"""
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class GameRules:
    """Lớp chứa logic game"""
    
    @staticmethod
    def calculate_result(move1, move2):
        """
        Tính kết quả trận đấu
        
        Args:
            move1: Nước đi của người chơi 1
            move2: Nước đi của người chơi 2
        
        Returns:
            1: Player 1 thắng
            -1: Player 2 thắng
            0: Hòa
        """
        if move1 == move2:
            return 0  # Hòa
        
        # Điều kiện thắng cho player 1
        if (move1 == Move.ROCK and move2 == Move.SCISSORS) or \
           (move1 == Move.PAPER and move2 == Move.ROCK) or \
           (move1 == Move.SCISSORS and move2 == Move.PAPER):
            return 1  # Player 1 thắng
        
        return -1  # Player 2 thắng
    
    @staticmethod
    def parse_move(move_str):
        """Chuyển đổi string thành Move"""
        try:
            return Move[move_str.upper()]
        except KeyError:
            return None
    
    @staticmethod
    def get_result_text(result):
        """
        Chuyển đổi kết quả thành text
        
        Args:
            result: 1, -1, hoặc 0
        
        Returns:
            Text mô tả kết quả
        """
        if result == 1:
            return "Bạn thắng!"
        elif result == -1:
            return "Bạn thua!"
        else:
            return "Hòa rồi!"
