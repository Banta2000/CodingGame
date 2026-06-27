import sys
HOME_PC = 1


def myPrint(*args):
    if HOME_PC:
        print(*args)
    else:
        print(*args, file=sys.stderr, flush=True)


def get_input() -> tuple:
    if HOME_PC:
        n_columns = 2
        n_rows = 2
        p1 = ["+ B#","  *#","C**#","####"]
        p2 = ["####","#**A","#*  ","#D +"]
        p3 = ["####","A**#","  *#","+ B#"]
        p4 = ["#D +","#*  ","#**C","####"]
        pieces = [p1, p2, p3, p4]


        n_columns = 8
        n_rows = 4

        f = open('input.txt', 'r')
        pieces = []
        for _ in range(n_columns * n_rows):
            tmp = []
            for _ in range(6):
                tmp.append(f.readline()[:-1])
            pieces.append(tmp)

        piece_size = len(pieces[0])
        n_pieces = len(pieces)
        

        
    else:
        # piece_size: size of a piece (its width and its height)
        # n_pieces: number of pieces (= nColumns * nRows)
        # n_columns: number of pieces in a row of the picture
        # n_rows: number of pieces in a column of the picture
        # picture_width: number of characters in a row of the picture (= 1 + nColumns * (pieceSize - 1))
        # picture_height: number of characters in a column of the picture (= 1 + nRows * (pieceSize - 1))
        piece_size, n_pieces = [int(i) for i in input().split()]
        n_columns, n_rows = [int(i) for i in input().split()]
        picture_width, picture_height = [int(i) for i in input().split()]
                
        pieces = []
        for i in range(n_pieces):
            piece = []
            for j in range(piece_size):
                piece.append(input())
            pieces.append(piece)

        if False:
            myPrint("piece_size, n_pieces, n_columns, n_rows, picture_width, picture_height")
            myPrint(piece_size, n_pieces, n_columns, n_rows, picture_width, picture_height)

            myPrint("pieces")
            for piece in pieces:
                myPrint("")
                for line in piece:
                    myPrint(line)

    return n_rows, n_columns, pieces


class Piece:
    def __init__(self, piece):
        self.size = len(piece)
        self.piece = piece
        self.edges = {}
        self.edges["top"] = self.piece[0]
        self.edges["bottom"] = self.piece[self.size - 1]
        self.edges["left"] = "".join([self.piece[i][0] for i in range(self.size)])
        self.edges["right"] = "".join([self.piece[i][self.size - 1] for i in range(self.size)])

    def __repr__(self) -> str:
        s = ""
        for line in self.piece:
            s += line + "\n"
        return s

    def find_matching_edge(self, edge):
        result = []
        if self.edges["top"] == edge:
            result.append(("top", "straight"))
        if self.edges["bottom"] == edge:
            result.append(("bottom", "straight"))
        if self.edges["left"] == edge:
            result.append(("left", "straight"))
        if self.edges["right"] == edge:
            result.append(("right", "straight"))
        if self.edges["top"] == edge[::-1]:
            result.append(("top", "reversed"))
        if self.edges["bottom"] == edge[::-1]:
            result.append(("bottom", "reversed"))
        if self.edges["left"] == edge[::-1]:
            result.append(("left", "reversed"))
        if self.edges["right"] == edge[::-1]:
            result.append(("right", "reversed"))
        return result

    # returns array with rotations options to match piece with desired edge on side
    def find_matching_edge_with_side(self, edge, side):
        result = []
        options = self.find_matching_edge(edge)
        for m_side, m_dir in options:
            if side == "top":
                if m_side == "top" and m_dir == "straight":
                    result.append(0)
                if m_side == "right" and m_dir == "straight":
                    result.append(1)
                if m_side == "bottom" and m_dir == "reversed":
                    result.append(2)
                if m_side == "left" and m_dir == "reversed":
                    result.append(3)
            if side == "right":
                if m_side == "right" and m_dir == "straight":
                    result.append(0)
                if m_side == "bottom" and m_dir == "reversed":
                    result.append(1)
                if m_side == "left" and m_dir == "reversed":
                    result.append(2)
                if m_side == "top" and m_dir == "straight":
                    result.append(3)
            if side == "bottom":
                if m_side == "bottom" and m_dir == "straight":
                    result.append(0)
                if m_side == "left" and m_dir == "straight":
                    result.append(1)
                if m_side == "top" and m_dir == "reversed":
                    result.append(2)
                if m_side == "right" and m_dir == "reversed":
                    result.append(3)
            if side == "left":
                if m_side == "left" and m_dir == "straight":
                    result.append(0)
                if m_side == "top" and m_dir == "reversed":
                    result.append(1)
                if m_side == "right" and m_dir == "reversed":
                    result.append(2)
                if m_side == "bottom" and m_dir == "straight":
                    result.append(3)
        return result

    # Rotate piece i times to the left
    def rotate_left(self, i = 0):
        for _ in range(i):
            new_piece = []
            for i in range(self.size):
                new_piece.append("".join([self.piece[j][self.size - 1 - i] for j in range(self.size)]))
            self.piece = new_piece
        self.edges["top"] = self.piece[0]
        self.edges["bottom"] = self.piece[self.size - 1]
        self.edges["left"] = "".join([self.piece[i][0] for i in range(self.size)])
        self.edges["right"] = "".join([self.piece[i][self.size - 1] for i in range(self.size)])


    def copy(self):
        new_piece = Piece(self.piece)
        return new_piece



class Game:
    def __init__(self, pieces, corner_piece) -> None:
        self.pieces = pieces
        self.piece_size = pieces[0].size
        self.pieces_num = len(pieces)
        self.board = {}
        for i in range(n_rows):
            for j in range(n_columns):
                self.board[(i, j)] = None
        self.board[(0, 0)] = self.find_corner_pieces()[corner_piece]

    def __repr__(self) -> str:
        # Board is a dict. Returns array of [](piece_num, rotation)]
        def _get_line_of_pieces(board, board_line):
            line_of_pieces = []
            for row in range(n_columns):
                line_of_pieces.append(board[(board_line, row)])
            return line_of_pieces

        # Returns array of string, each line / string is a line in the picture
        def _assemble_line_of_pieces(line_of_pieces):
            s = ["" for _ in range(self.piece_size)]
            for entry in line_of_pieces:
                if entry is None:
                    for i in range(self.piece_size):
                        s[i] += "".join(["." for _ in range(self.piece_size-1)])
                else:
                    piece_num, rotation = entry
                    temp_piece = self.pieces[piece_num].copy()
                    temp_piece.rotate_left(rotation)
                    for i, line in enumerate(temp_piece.piece):
                        s[i] += line[:-1]
            for i, line in enumerate(s):
                s[i] += "#"
            return s

        endresult = []
        for line_of_board in range(n_rows):
            line_of_pieces = _get_line_of_pieces(self.board, line_of_board)
            endresult += _assemble_line_of_pieces(line_of_pieces)[:-1]
        endresult.append(endresult[0])
        endresult = "\n".join(endresult) 
        return endresult

    def find_corner_pieces(self):
        res = []
        end_edge = "".join(["#" for _ in range(self.piece_size)])
        res += [(piece_num, 0) for piece_num, piece in enumerate(self.pieces) if piece.edges["top"] == end_edge and piece.edges["left"] == end_edge]
        res += [(piece_num, 1) for piece_num, piece in enumerate(self.pieces) if piece.edges["top"] == end_edge and piece.edges["right"] == end_edge]
        res += [(piece_num, 2) for piece_num, piece in enumerate(self.pieces) if piece.edges["bottom"] == end_edge and piece.edges["right"] == end_edge]
        res += [(piece_num, 3) for piece_num, piece in enumerate(self.pieces) if piece.edges["bottom"] == end_edge and piece.edges["left"] == end_edge]
        return res

    # Returns array with (string, edge_label) ex [("a2d3", top), ..]
    def get_requirements_for_position(self, pos):
        def _get_edge(pos, side):
            counterEdge = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}
            counterEdge = counterEdge[side]
            if pos not in board:
                # print("piece not on board, returning ####")
                return [("".join(["#" for _ in range(self.piece_size)]), counterEdge)] 
            if pos in board and board[pos] is not None:
                piece_num, rotation = board[pos]
                temp_piece = pieces[piece_num].copy()
                temp_piece.rotate_left(rotation)
                edge = temp_piece.edges[side]
                # print("piece on board, returning ", side, " edge:", edge)
                return [(edge, counterEdge)]
            return []
            
        row, col = pos
        board = self.board
        pieces = self.pieces

        top_pos = (row - 1, col)
        right_pos = (row, col + 1)
        bottom_pos = (row + 1, col)
        left_pos = (row, col - 1)

        res = []
        res += _get_edge(top_pos, "bottom")
        res += _get_edge(right_pos, "left")
        res += _get_edge(bottom_pos, "top")
        res += _get_edge(left_pos, "right")
        return res

    # Returs array with (piecen_num, rotation) for all pieces that match this edge
    def find_pieces_with_single_matching_edge(self, edge, side):
        result = []
        for piece_num, piece in enumerate(self.pieces):
            rotation_options = piece.find_matching_edge_with_side(edge, side)
            options = [(piece_num, r) for r in rotation_options]
            result += options
        return result

    # Returns array with (piecen_num, rotation) for all pieces that match all edges
    def find_pieces_with_multiple_matching_edges(self, requirements):
        res_counter = {}
        for edge, side in requirements:
            options = self.find_pieces_with_single_matching_edge(edge, side)
 #           print("looking for", edge, side, "found", options)
            for option in options:
                if option not in res_counter:
                    res_counter[option] = 0
                res_counter[option] += 1
 #       print("final counter", res_counter)
        final_options = [option for option in res_counter if res_counter[option] == len(requirements)]
 #       print("final winners", final_options)
        return final_options

    # Finds possible solutions for pos and then calls itself for every solution
    def dfs(self, piece_num):
        global solution

        if piece_num == self.pieces_num:
            solution = {k:v for k, v in self.board.items()}
            
        row = piece_num // n_columns
        col = piece_num % n_columns
        pos = (row, col)

        reqs = self.get_requirements_for_position(pos)
        options = self.find_pieces_with_multiple_matching_edges(reqs)
        used_pieces = [v[0] for k, v in self.board.items() if v is not None]
        options = [option for option in options if option[0] not in used_pieces]

#        print("looking for", piece_num, "at", pos, "with reqs", reqs, "found options:", len(options))

        for option in options:
            self.board[pos] = option
            self.dfs(piece_num + 1)
            self.board[pos] = None


    def is_first_piece_correctly_oriented(self):
        rotation = [rot for piece, rot in self.board.values() if piece == 0][0]
        return rotation == 0


# ********************************************************

n_rows, n_columns, raw_pieces = get_input()
pieces = [Piece(p) for p in raw_pieces]
solution = {}

for cornerpiece in range(4):
    game = Game(pieces, cornerpiece)
    game.dfs(1)
    game.board = solution
    if solution and game.is_first_piece_correctly_oriented():
        break

print(game)
