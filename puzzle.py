import sys
HOME_PC = 1


def myPrint(*args):
    print(*args, file=sys.stderr, flush=True)


def get_input() -> tuple:
    if HOME_PC:
        piece_size = 4
        n_pieces = 4
        n_columns = 2
        n_rows = 2
        picture_width = 7
        picture_height = 7
        p1 = ["+ B#","  *#","C**#","####"]
        p2 = ["####","#**A","#*  ","#D +"]
        p3 = ["####","A**#","  *#","+ B#"]
        p4 = ["#D +","#*  ","#**C","####"]
        pieces = [p1, p2, p3, p4]
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

        if True:
            print("piece_size, n_pieces, n_columns, n_rows, picture_width, picture_height")
            print(piece_size, n_pieces, n_columns, n_rows, picture_width, picture_height)

            print("pieces")
            for piece in pieces:
                print("")
                for line in piece:
                    print(line)

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
    def __init__(self, pieces) -> None:
        self.pieces = pieces
        self.piece_size = pieces[0].size
        self.pieces_num = len(pieces)
        self.board = {}
        self.board[(0,0)] = (1, 0)
        self.board[(0,1)] = (2, 0)
        self.board[(1,0)] = (3, 0)
        self.board[(1,1)] = (0, 0)

    def __repr__(self) -> str:
        def _get_line_of_pieces(board, board_line):
            line_of_pieces = []
            for row in range(n_rows):
                line_of_pieces.append(board[(board_line, row)])
            return line_of_pieces
        
        def _assemble_line_of_pieces(line_of_pieces):
            s = ["" for _ in range(self.piece_size)]
            for piece_num, rotation in line_of_pieces:
                temp_piece = self.pieces[piece_num].copy()
                temp_piece.rotate_left(rotation)
                for i in range(self.piece_size):
                    s[i] += temp_piece.piece[i]                    
            return s

        endresult = []
        for line_of_board in range(n_rows):
            line_of_pieces = _get_line_of_pieces(self.board, line_of_board)
            new_s = _assemble_line_of_pieces(line_of_pieces)
            new_s = "\n".join(new_s)
            endresult.append(new_s)
        endresult = "\n".join(endresult) 
        return endresult
        
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



# ********************************************************

n_rows, n_columns, raw_pieces = get_input()
pieces = [Piece(p) for p in raw_pieces]
game = Game(pieces)

for p in pieces: print(p)
p = pieces[0]

e = "+ B#"
e = "#B +"

e1 = "+ C#"
e2 = "####"

print(game)

game.board[(0, 1)] = None

p = (0, 0)
r = game.get_requirements_for_position(p)
print(r)

#TODO get_requirements_for_position gibt mir ein array mit edges (und
# deren bennenung die ich benutzen kann um das richtige teil zu filtern.
# wichtig ist, dass die leeren felder der Matrize mit None gefüllt sind
# nun kan nich ein teil setzen, und nach dem nächsten teil suchen


""" num_pieces = len(pieces)
for piece_i in range(num_pieces):
    row = piece_i // n_columns
    col = piece_i % n_columns
    center_p = (row, col)
    print("Examining", row, col, game.board[(row, col)])
    
    

    print("")
        
 """    
    
