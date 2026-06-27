HOME_PC = True


from Point2D import Point2D
from typing import Any, Tuple, List
from Board import Board


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
        self.breaker: bool = False

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
        if self.get_char_ahead() == WALL:
            return False
        if self.get_char_ahead() == OBSTACLE:
            return self.breaker
        return True


def get_start_parameters():
    if HOME_PC:
        data1 = [
            "##########",
            "#        #",
            "#  S   W #",
            "#        #",
            "#  $     #",
            "#        #",
            "#@       #",
            "#        #",
            "#E     N #",
            "##########",
        ]

        data2 = [
            "########",
            "# @    #",
            "#     X#",
            "# XXX  #",
            "#   XX #",
            "#   XX #",
            "#     $#",
            "########",
        ]

        data3 = [
            "########",
            "#     $#",
            "#      #",
            "#      #",
            "#  @   #",
            "#      #",
            "#      #",
            "########",
        ]

        data4 = [
            "########",
            "#      #",
            "# @    #",
            "# XX   #",
            "#  XX  #",
            "#   XX #",
            "#     $#",
            "########",
        ]

        data6 = [
            "##########",
            "# @      #",
            "# B      #",
            "#XXX     #",
            "# B      #",
            "#    BXX$#",
            "#XXXXXXXX#",
            "#        #",
            "#        #",
            "##########",
        ]

        data7 = [
            "##########",
            "#    I   #",
            "#        #",
            "#       $#",
            "#       @#",
            "#        #",
            "#       I#",
            "#        #",
            "#        #",
            "##########",
        ]

        data8 = [
            "##########",
            "#    T   #",
            "#        #",
            "#        #",
            "#        #",
            "#@       #",
            "#        #",
            "#        #",
            "#    T  $#",
            "##########",
        ]

        data11 = [
            "###############",
            "#      IXXXXX #",
            "#  @          #",
            "#E S          #",
            "#             #",
            "#  I          #",
            "#  B          #",
            "#  B   S     W#",
            "#  B   T      #",
            "#             #",
            "#         T   #",
            "#         B   #",
            "#N          W$#",
            "#        XXXX #",
            "###############",
        ]

        data12 = [
            "###############",
            "#  #@#I  T$#  #",
            "#  #    IB #  #",
            "#  #     W #  #",
            "#  #      ##  #",
            "#  #B XBN# #  #",
            "#  ##      #  #",
            "#  #       #  #",
            "#  #     W #  #",
            "#  #      ##  #",
            "#  #B XBN# #  #",
            "#  ##      #  #",
            "#  #       #  #",
            "#  #     W #  #",
            "#  #      ##  #",
            "#  #B XBN# #  #",
            "#  ##      #  #",
            "#  #       #  #",
            "#  #       #  #",
            "#  #      ##  #",
            "#  #  XBIT #  #",
            "#  #########  #",
            "#             #",
            "# ##### ##### #",
            "# #     #     #",
            "# #     #  ## #",
            "# #     #   # #",
            "# ##### ##### #",
            "#             #",
            "###############",
        ]

        data = data11

    else:
        l, c = [int(i) for i in input().split()]
        data = [input() for _ in range(l)]
    board = Board()
    board.load_data(data)
    return board


def generate_key(player: Player, board: Board):
    # Convert the board into a single string
    # This is a simple representation, you might want to use a more complex one
    s = ""
    for r in range(board.num_rows):
        for c in range(board.num_cols):
            p = Point2D(r, c)
            s += board.board[p]
    key = (player.pos.row, player.pos.col, player.dir, player.breaker, s)
    return key


# ********************************************************

DEBUG = False

WALL = "#"
OBSTACLE = "X"
BEER = "B"
EXIT = "$"
INVERTER = "I"
TELEPORTER = "T"
MAPPER = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST"}

BOARD = get_start_parameters()
# BOARD.print()

player = Player(board=BOARD, start=BOARD.find("@")[0], direction="S")

visited = set()
history = []

while True:
    if DEBUG:
        player.print()

    # Check for loop
    key = generate_key(player, BOARD)
    if key in visited:
        if DEBUG:
            print("Loop detected, breaking out of the loop.")
        history = ["LOOP"]
        break
    visited.add(key)

    # If wall ahead, turn in turn_order until the path is clear (depends on breaker)
    if not player.is_clear_ahead():
        player.turn_until_is_clear()
        if DEBUG:
            print("Turning, now facing", player.dir)
        continue

    # If Breaker and obstacle ahead, break the obstacle
    if player.get_char_ahead() == OBSTACLE and player.breaker:
        if DEBUG:
            print("Breaking obstacle at", player.get_pos_ahead())
        BOARD[player.get_pos_ahead()] = " "

    player.advance()
    history.append(MAPPER[player.dir])

    # ***** If advance was successful, we immediately proces conditions when entering special fields

    # If turn field
    if player.get_char_at_self_pos() in ["S", "E", "N", "W"]:
        player.set_direction(player.get_char_at_self_pos())
        if DEBUG:
            print("Forcing turn, now facing", player.dir)
        continue

    # If exit found
    if player.get_char_at_self_pos() == EXIT:
        if DEBUG:
            print("Exit found at", player.pos)
        break

    # If beaker field
    if player.get_char_at_self_pos() == BEER:
        if DEBUG:
            print("Beaker found at", player.pos)
        player.breaker = not player.breaker
        continue

    # If inverter field
    if player.get_char_at_self_pos() == INVERTER:
        if DEBUG:
            print("Inverter found at", player.pos)
        player.turn_order = player.turn_order[::-1]
        continue

    # If Teleporter field
    if player.get_char_at_self_pos() == TELEPORTER:
        if DEBUG:
            print("Teleporter found at", player.pos)
        # Find all teleporters
        teleporters = BOARD.find("T")
        target_teleporter = [x for x in teleporters if player.pos != x][0]
        player.pos = target_teleporter
        continue


for line in history:
    print(line)
