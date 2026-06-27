# THIS IS A CLASS THAT WAS USED SPECIFICALLY FOR THE BLUNDER PROJECT
# IT NEEDS TO BE CLEANED AND MADE MORE GENERIC; SPECIALLY THE TURNING METHODS
# ARE CURRENTLY NOT SET TO BE TURN_LEFT OR TURN_RIGHT
# BUT THE BASIC SCELETTON IS HERE

from Board import Board
from Point2D import Point2D
from typing import List, Tuple, Any, Optional


class Player:
    """
    A player is a Point2D with a direction and a board.
    Direction: "N", "S", "E", "W"
    """

    def __init__(self, board: Board, start: Point2D, direction: str) -> None:
        self.board: Board = board
        self.pos: Point2D = start
        self.dir: str = direction
        self.turn_order: List[str] = ["S", "E", "N", "W"]
        self.OBSTACLES = "X"

    def __repr__(self) -> str:
        return f"Player({self.pos}, {self.dir})"

    def advance(self) -> None:
        """Advances the player in the current direction."""
        if self.dir == "N":
            self.pos = self.pos.up()
        elif self.dir == "S":
            self.pos = self.pos.down()
        elif self.dir == "E":
            self.pos = self.pos.right()
        elif self.dir == "W":
            self.pos = self.pos.left()

    def get_pos_ahead(self) -> Point2D:
        """Get the next position without moving."""
        if self.dir == "N":
            return self.pos.up()
        elif self.dir == "S":
            return self.pos.down()
        elif self.dir == "E":
            return self.pos.right()
        elif self.dir == "W":
            return self.pos.left()
        return self.pos

    def get_char_at_self_pos(self) -> str:
        """Get the character at the players current position."""
        if self.pos in self.board:
            return self.board[self.pos]
        else:
            raise KeyError(f"Position {self.pos} is not on the board")

    def get_char_ahead(self) -> str:
        """Get the character at the position ahead without moving."""
        pos_ahead = self.get_pos_ahead()
        if pos_ahead in self.board:
            return self.board[pos_ahead]
        else:
            raise KeyError(f"Position {pos_ahead} is not on the board")

    def get_char_at_direction(self, direction: str) -> str:
        """Get the character at the position in the given direction."""
        if direction not in ["N", "S", "E", "W"]:
            raise ValueError(f"Invalid direction: {direction}. Must be one of [N, S, E, W].")

        pos = self.pos
        mapper = {"N": pos.up(), "S": pos.down(), "E": pos.right(), "W": pos.left()}
        pos_at_direction = mapper[direction]

        if pos_at_direction not in self.board:
            raise KeyError(f"Position {pos_at_direction} is not on the board")

        char_at_direction = self.board[pos_at_direction]
        return char_at_direction

    def set_direction(self, direction: str) -> None:
        """Set the direction of the player."""
        if direction in ["N", "S", "E", "W"]:
            self.dir = direction
        else:
            raise ValueError(f"Invalid direction: {direction}. Must be one of [N, S, E, W].")

    def turn_until_is_clear(self) -> None:
        """Turn the player in turn_order until path is clear (obstacle depends on breaker)."""
        for dir in self.turn_order:
            self.set_direction(dir)
            if self.is_clear_ahead():
                return

    def print(self) -> None:
        """Print the current position and direction of the player."""
        print(f"Player at {self.pos} facing {self.dir}")

    def is_clear_ahead(self) -> bool:
        """Check if the path ahead is clear. If Wall: False. If Obstacle: Depends on breaker."""
        if self.get_char_ahead() == self.OBSTACLES:
            return False
        return True
