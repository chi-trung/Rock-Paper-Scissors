"""
Logic và luật chơi Oẳn Tù Tì (Rock – Paper – Scissors)
"""
from enum import Enum
from typing import Optional


class Move(Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class GameRules:
    """Xử lý luật chơi"""

    # Bảng quy định nước nào thắng nước nào
    WIN_MAP = {
        Move.ROCK: Move.SCISSORS,
        Move.PAPER: Move.ROCK,
        Move.SCISSORS: Move.PAPER,
    }

    @staticmethod
    def calculate_result(player1: Move, player2: Move) -> int:
        """
        Xác định kết quả trận đấu

        Returns:
            1  : Player 1 thắng
            -1 : Player 2 thắng
            0  : Hòa
        """
        if player1 == player2:
            return 0

        if GameRules.WIN_MAP[player1] == player2:
            return 1

        return -1

    @staticmethod
    def parse_move(move_str: str) -> Optional[Move]:
        """Chuyển chuỗi nhập vào thành Move"""
        if not move_str:
            return None

        move_str = move_str.strip().upper()
        return Move.__members__.get(move_str)

    @staticmethod
    def get_result_text(result: int) -> str:
        """Trả về thông báo kết quả"""
        messages = {
            1: "Bạn thắng!",
            -1: "Bạn thua!",
            0: "Hòa rồi!"
        }
        return messages.get(result, "Kết quả không hợp lệ")
