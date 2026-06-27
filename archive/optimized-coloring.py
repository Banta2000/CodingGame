from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper
import sys
import os
from typing import Any, Tuple, List
from itertools import permutations
from typing import Optional


HOME_PC = False
Point = Tuple[int, int]
Board = dict[Point, Any]


class DLNode:
    def __init__(self, id, required=True):
        """
        Initialize a doubly linked node.
        """
        self.id = id
        self.required = required
        self.left: DLNode = self
        self.right: DLNode = self
        self.up: DLNode = self
        self.down: DLNode = self
        self.col_head: DLNode = self
        self.row_head: DLNode = self
        self.len: int = 0

    def __repr__(self):
        u_str = f"U: {self.up.id}" if self.up else "U: None"
        d_str = f"D: {self.down.id}" if self.down else "D: None"
        l_str = f"L: {self.left.id}" if self.left else "L: None"
        r_str = f"R: {self.right.id}" if self.right else "R: None"
        row_head_str = f"RowHead: {self.row_head.id}" if self.row_head else "RowHead: None"
        col_head_str = f"ColHead: {self.col_head.id}" if self.col_head else "ColHead: None"
        len_str = f"Len: {self.len}"
        res = f"{self.id} | {u_str} | {d_str} | {l_str} | {r_str} | {len_str} | {row_head_str} | {col_head_str}"
        return res

    def insert_right(self, new_node: "DLNode"):
        """
        Insert a node to the right of the current node.
        Adopt the self's row_head. Don't update the row_head length.
        """
        self.right.left = new_node
        new_node.right = self.right
        self.right = new_node
        new_node.left = self
        if self.row_head is not None:
            new_node.row_head = self.row_head

    def insert_left(self, new_node: "DLNode"):
        """
        Insert a node to the left of the current node.
        Adopt the self's row_head. Don't update the row_head length.
        """
        self.left.right = new_node
        new_node.left = self.left
        self.left = new_node
        new_node.right = self
        if self.row_head is not None:
            new_node.row_head = self.row_head

    def insert_up(self, new_node: "DLNode", col_head: Optional["DLNode"] = None):
        """
        Insert a node above the current node. Update the col_head length.
        Adopt the self's col_head is and increase its length.
        """
        self.up.down = new_node
        new_node.up = self.up
        self.up = new_node
        new_node.down = self
        if self.col_head is not None:
            new_node.col_head = self.col_head
            new_node.col_head.len += 1

    def insert_down(self, new_node: "DLNode", col_head: Optional["DLNode"] = None):
        """
        Insert a node below the current node. Update the col_head length.
        Adopt the self's col_head is and increase its length.
        """
        self.down.up = new_node
        new_node.down = self.down
        self.down = new_node
        new_node.up = self
        if self.col_head is not None:
            new_node.col_head = self.col_head
            new_node.col_head.len += 1

    def remove(self):
        """
        Remove the current node from the list. Only hides the node from the col, not from the row.
        """
        if self.left.right != self or self.right.left != self or self.up.down != self or self.down.up != self:
            raise ValueError("Node is already removed or corrupted.")
        # self.left.right = self.right
        # self.right.left = self.left
        self.up.down = self.down
        self.down.up = self.up

    def remove_up_down(self):
        """
        Remove the node's connections to top and bottom nodes; not to left and right nodes.
        """
        if self.up.down != self or self.down.up != self:
            return
            # raise ValueError("Node is already removed or corrupted.")
        self.up.down = self.down
        self.down.up = self.up
        self.col_head.len -= 1

    def remove_left_right(self):
        """
        Remove the node's connections to left and right nodes; not to top and bottom nodes.
        Don't update any lengths.
        """
        if self.left.right != self or self.right.left != self:
            # Node is already removed
            return
        self.left.right = self.right
        self.right.left = self.left

    def restore_up_down(self):
        """
        Re-inserts the node by restoring the up-down relationships. Increases col_head length.
        """
        if self.up.down == self or self.down.up == self:
            # Node is already restored
            return
        self.up.down = self
        self.down.up = self
        self.col_head.len += 1

    def restore_left_right(self):
        """
        Re-inserts the node by restoring the left-right relationships. Don't update length.
        """
        if self.left.right == self or self.right.left == self:
            # Node is already restored
            return
        self.left.right = self
        self.right.left = self


class AlgoXSolver:
    def __init__(self):
        self.root = DLNode("root")
        self.all_solutions = []
        self.stop_at_first = False

    def add_requirements(self, requirement_ids, required=True):
        """
        Add required requirements (columns) to the header row. Required is boolen to indicate if the requirements are required or optional.
        """
        curr = self.root.left
        for req_id in requirement_ids:
            tmp = DLNode(req_id, required)
            curr.insert_right(tmp)
            curr = tmp

    def add_actions(self, action_rows: dict):
        """
        Add action rows to the table.
        :param action_rows: A dictionary where keys are row IDs and values are lists of column IDs.
        """
        for row_id, col_ids in action_rows.items():
            self.add_row(row_id, col_ids)

    def add_row(self, row_id: tuple, row_data: list):
        """
        Add a new row to the table. row_data must be a list of values that match the values in the header row.
        If row_id is None, then the row's header will be an increasing number starting from 0.
        """
        # Check if all elements of row_data are in header row; convert first to set for faster lookup
        header_values = set()
        curr = self.root.right
        while curr != self.root:
            header_values.add(curr.id)
            curr = curr.right
        row_data_not_in_header = [x for x in row_data if x not in header_values]
        if row_data_not_in_header:
            raise ValueError(f"Row data {row_data_not_in_header} not in header row. Full row: {row_data}")

        # Ensure row_id is not already in the table (avoid duplicate rows)
        if row_id is not None:
            curr = self.root.down
            while curr != self.root:
                if curr.id == row_id:
                    raise ValueError(f"Row ID {row_id} already exists. Cannot add duplicate rows.")
                curr = curr.down

        # Create and add row_header for the new row
        row_head = DLNode(row_id)
        self.root.insert_up(row_head)

        # Go through header row; if header_row.id is in row_data, add node to row and column, else skip
        col_head = self.root.right
        while col_head != self.root:
            if col_head.id in row_data:
                self.add_node_to_row_and_column(row_head, col_head)
            col_head = col_head.right

    def add_node_to_row_and_column(self, row_head: DLNode, col_head: DLNode):
        """
        Add new node to the bottom right, increment length of column by 1.
        """
        new_node = DLNode(1)
        col_head.insert_up(new_node)
        row_head.insert_left(new_node)

    def remove_row(self, anchor: DLNode, keep_anchored: bool = False):
        """
        Remove row from table by breaking up-down relationship of each node in row.
        The left-right relationship of nodes  is preserved.
        If keep_anchored then exclude (= preserve) up-down relationships of anchor so we can backtrack.
        """
        # Jump to row_head, remove up-down relationship of row_head
        row_head = anchor.row_head
        row_head.remove_up_down()

        # Iterate over all nodes in the row (excluding the anchor), start with row head and move right
        # Do not break-up the up-down relationship of the anchor node
        current = row_head.right
        while current != row_head:
            if not keep_anchored or (keep_anchored and current != anchor):
                current.remove_up_down()
            current = current.right

    def restore_row(self, row_head: DLNode):
        """
        Restore up-down connections of row. Traverse inverse order; row_col is last.
        """
        row_head = row_head.row_head
        curr = row_head.left
        while curr != row_head:
            curr.restore_up_down()
            curr = curr.left

        # Finally, restore the row header itself (up-down relationship)
        curr.restore_up_down()

    def remove_col_and_rows(self, anchor: DLNode):
        """
        Travel down column; remove all rows (remove up-down relationships of all nodes except travel col).
        """
        # Jump to col_head, remove its left-right relationship
        col_head = anchor.col_head
        col_head.remove_left_right()

        # Remove all rows that have a node in this column, except the anchor node
        curr = col_head.down
        while curr != col_head:
            self.remove_row(curr, keep_anchored=True)
            curr = curr.down

    def restore_col_and_rows(self, anchor: DLNode):
        """
        Travel upwards column, restore all rows that have a node in this column
        """
        col_head = anchor.col_head
        curr = col_head.up
        while curr != col_head:
            self.restore_row(curr)
            curr = curr.up

        # Finally, restore the col header itself (left-right relationship)
        col_head.restore_left_right()

    def select_next_column(self):
        """
        Select the required column with the fewest nodes (smallest len). Returns col_head.
        Only considers columns where col_head.required is True.
        """
        col_head = self.root.right
        min_col = None
        while col_head != self.root:
            if getattr(col_head, "required", True):
                if min_col is None or col_head.len < min_col.len:
                    min_col = col_head
            col_head = col_head.right
        return min_col

    def remove_row_col_and_rows(self, anchor: DLNode):
        """
        For row, go through each column and remove the col with all its rows.
        """
        row_head = anchor.row_head
        row_head.remove_up_down()

        curr = row_head.right
        while curr != row_head:
            # Remove the column and all rows that have a node in this column
            self.remove_col_and_rows(curr)
            curr = curr.right

    def restore_row_col_and_rows(self, anchor: DLNode):
        """
        For row, go through each column and restore the col with all its rows.
        """
        row_head = anchor.row_head
        curr = row_head.left
        while curr != row_head:
            # Restore the column and all rows that have a node in this column
            self.restore_col_and_rows(curr)
            curr = curr.left

        # Finally, restore the row header itself (up-down relationship)
        row_head.restore_up_down()

    def execute_action(self, row_id: tuple):
        """
        Execute a specific action (row) in the Dancing Links table.
        """
        # Find the row header for the row_id
        row_head = self.root.down
        while row_head != self.root:
            if row_head.id == row_id:
                break
            row_head = row_head.down
        else:
            raise ValueError(f"Row ID {row_id} does not exist in the table.")

        self.remove_row_col_and_rows(row_head)

    def solve(self):
        yield from self.solve_matrix()

    def solve_matrix(self, solution=None):
        """
        Recursive implementation of Algorithm X to solve the exact cover problem.
        :param solution: List of rows that form the current partial solution.
        :return: A list of rows that form a complete solution, or None if no solution exists.
        """
        if solution is None:
            solution = []

        # Check if all required columns are covered (base case)
        # Only required columns should be considered for solution completion
        col_head = self.root.right
        while col_head != self.root:
            if getattr(col_head, "required", True):
                # If any required column remains, not a complete solution
                break
            col_head = col_head.right
        else:
            # All required columns are covered
            res = [x.row_head.id for x in solution]
            yield res
            return

        # Step 1: Choose a column to cover (heuristic: column with the fewest nodes)
        col_to_cover_head = self.select_next_column()

        # Step 2: Try every row in the selected column
        col_travelor = col_to_cover_head.down
        while col_travelor != col_to_cover_head:
            # col_travelor is the anchor for the row that we are choosing, we will remove this row

            # Step 3: Add the row to the solution
            solution.append(col_travelor)

            # Step 4: Cover all columns that have a node in this row
            self.remove_row_col_and_rows(col_travelor)

            # Step 5: Recursively call solve with the updated solution
            yield from self.solve_matrix(solution)

            # Step 6: Backtrack, uncover the columns and remove the row from the solution
            self.restore_row_col_and_rows(col_travelor)
            solution.pop()

            # Move to the next row
            col_travelor = col_travelor.down

        # No solution found
        return False

    def print_header_row(self):
        """
        Print the header row for debugging.
        """
        current = self.root
        while True:
            print(current.id, end=" -> ")
            current = current.right
            if current == self.root:
                break

    def print_rows(self):
        """
        Print the rows (actions) for debugging.
        """
        current = self.root.down
        while current != self.root:
            print(current.id, end=" -> ")
            current = current.down
            if current == self.root:
                break
        print()

    def print_table_simple(self):
        """
        Print the entire table for debugging.
        """
        # Print the header row
        print("Header Row:")
        self.print_header_row()

        # Print each row
        print("\nRows:")
        row = self.root.down
        while row != self.root:
            print(f"Row {row.id}: ", end="")
            node = row.right
            while node != row:
                print(node.col_head.id, end=" ")
                node = node.right
            print()
            row = row.down
        print()

    def print_table(self):
        """
        Print the entire Dancing Links table as an aligned ASCII table.
        """
        # Collect header row
        headers = []
        current = self.root.right
        while current != self.root:
            headers.append(current.id)
            current = current.right

        # Determine column widths
        col_widths = {header: max(len(str(header)), 2) for header in headers}
        row = self.root.down
        while row != self.root:
            node = row.right
            while node != row:
                col_widths[node.col_head.id] = max(col_widths[node.col_head.id], len(str(node.col_head.id)))
                node = node.right
            row = row.down

        # Print header row
        header_row = "root".ljust(6) + " | " + " | ".join(str(header).ljust(col_widths[header]) for header in headers)
        print(header_row)
        print("-" * len(header_row))

        # Print each row
        row = self.root.down
        while row != self.root:
            row_data = {header: " " for header in headers}
            node = row.right
            while node != row:
                row_data[node.col_head.id] = "X"
                node = node.right
            row_line = (
                str(row.id).ljust(6)
                + " | "
                + " | ".join(row_data[header].ljust(col_widths[header]) for header in headers)
            )
            print(row_line)
            row = row.down
        print()


def explore_island(board, p):
    def _get_empty_neighbours(board, p):
        r, c = p
        neighbours = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        neighbours = [p for p in neighbours if p in board]
        neighbours = [p for p in neighbours if board[p] == " "]
        return neighbours

    stack = [p]
    visited = set()
    while stack:
        p = stack.pop()
        if p in visited:
            continue
        visited.add(p)
        for n in _get_empty_neighbours(board, p):
            if n not in visited:
                stack.append(n)
    return visited


# Return next empty cell
def get_next_empty(board):
    for p, c in board.items():
        if c == " ":
            return p
    return None


# Paints the board with island ids and returns list of islands
def get_all_islands(board):
    islands = []
    next_island_id = 0
    while True:
        p = get_next_empty(board)
        if p is None:
            break
        island_fields = explore_island(board, p)
        islands.append(island_fields)
        for p in island_fields:
            board[p] = next_island_id
        next_island_id += 1
    return islands


# Returns the 2-distance neighbours of a field
def find_neighbour_islands_of_one_field(board, p):
    r, c = p
    # Potential neighbors at distance 2
    checks = [((r - 1, c), (r - 2, c)), ((r + 1, c), (r + 2, c)), ((r, c - 1), (r, c - 2)), ((r, c + 1), (r, c + 2))]
    res = set()
    for mid, end in checks:
        if end in board and mid in board:
            # Rule: separated by a SINGLE non-space character
            if not isinstance(board[mid], int) and board[mid] != " ":
                res.add(board[end])
    return res


# Checks al fields of an island and returns 2-distance neigbours
def find_neighbours_islands_if_one_island(board, island):
    res = set()
    current_island_id = board[list(island)[0]]
    for p in island:
        neighbours = find_neighbour_islands_of_one_field(board, p)
        res.update(neighbours)

    # We only care about other islands (integers)
    actual_neighbours = {n for n in res if isinstance(n, int) and n != current_island_id}
    return actual_neighbours


def create_graph(board, islands):
    graph = {}
    for i, island in enumerate(islands):
        island_ref = list(island)[0]
        island_id = board[island_ref]
        neighbours = find_neighbours_islands_if_one_island(board, island)
        graph[island_id] = neighbours
    return graph


def generate_hard_requirements():
    # Every island must have one color: ("one_col", island_id)   ("one_col", a)
    every_island_one_color = [("one_col", x) for x in island_ids]
    return every_island_one_color


def generate_soft_requirements() -> list[tuple]:
    # two neighbouring islands cannot have the same color
    # ("same_col", color, island_id1, island_id2)
    # ("same_col", a, a, b)
    all_pairs_set = set()
    for islands in island_ids:
        for neighbour in graph[islands]:
            pair = tuple(sorted([islands, neighbour]))
            all_pairs_set.add(pair)

    all_pairs = sorted(list(all_pairs_set))

    res: list[tuple[Any, ...]] = []
    for color in colors:
        for x, y in all_pairs:
            res.append(("same_col", color, x, y))
    return res


def generate_action_keys():
    # Generate all possible actions without requirements, just keys
    # Use is_valid_action() to check if action is valid
    result = []
    for color in colors:
        for island in island_ids:
            result.append((island, color))
    return result


def map_action_to_requirements(action):
    island, color = action

    # Island has a color
    res = [("one_col", island)]

    # Island and its neighbours have this color
    for neighbour in graph[island]:
        a, b = sorted([island, neighbour])
        res.append(("same_col", color, a, b))
    return res


def generate_actions_mapped_to_requirements():
    actions = generate_action_keys()
    res = {action: map_action_to_requirements(action) for action in actions}
    return res


def print_DLList(root: DLNode):
    """
    Print the doubly linked list starting from the root node.
    """
    if root is None:
        print("The list is empty.")
        return
    current = root
    while True:
        print(current)
        current = current.right
        if current == root:
            break


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


def read_input(CGH: CodingGameHelper):
    w = int(CGH.input())
    h = int(CGH.input())
    data = [CGH.input() for _ in range(h)]

    board = {}
    for r, line in enumerate(data):
        # Pad line with spaces to ensure it has width w
        padded_line = line.ljust(w)
        for c, char in enumerate(padded_line):
            board[(r, c)] = char
    return board


def printBoard(board):
    rows = max(r for r, c in board)
    cols = max(c for r, c in board)
    for r in range(rows + 1):
        for c in range(cols + 1):
            myPrint(board.get((r, c), " "), end="")
        myPrint()
    myPrint()


# ********************************************************

for i in range(1, 9):
    CGH = CodingGameHelper(i, __file__)
    board = read_input(CGH)
    islands = get_all_islands(board)
    graph = create_graph(board, islands)
    island_ids = list(graph.keys())

    num_colors = 1
    while True:
        colors = [x for x in range(1, num_colors + 1)]
        colors = [str(x) for x in colors]

        HARD_REQUIREMENTS = generate_hard_requirements()
        SOFT_REQUIREMENTS = generate_soft_requirements()
        ACTIONS = generate_actions_mapped_to_requirements()

        solver = AlgoXSolver()
        solver.add_requirements(HARD_REQUIREMENTS, required=True)
        solver.add_requirements(SOFT_REQUIREMENTS, required=False)
        solver.add_actions(ACTIONS)

        try:
            solution = next(solver.solve())
            break
        except StopIteration:
            num_colors += 1
            continue

    # print(num_colors)
    CGH.add_output_line(num_colors)
    CGH.assert_output()
