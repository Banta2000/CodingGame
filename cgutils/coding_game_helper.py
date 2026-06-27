import os

# Initiate the Helper Class with either the test case number - or keep empty to read web input
# CGH = CodingGameHelper(case_nr, __file__)
# Puzzle-specific input parsing should stay in the puzzle file.
# This helper only abstracts where the raw lines come from and how output is checked.
# CGH.add_output_line(len(islands))
# CGH.add_output_line(len(unique_shapes))
# CGH.assert_output(verbose=True)


class CodingGameHelper:
    def __init__(self, case_nr=None, puzzle_file=None):
        self.case_nr = case_nr
        self.puzzle_file = puzzle_file
        self.actual_output_lines = []
        self.expected_output_lines = []

        if case_nr is None:
            self.from_web = True
            self.input_lines = None
            self.line_index = 0
        else:
            self.from_web = False
            self.input_lines = self._read_input_lines_from_file(case_nr)
            self.expected_output_lines = self._read_output_lines_from_file(case_nr)
            self.line_index = 0

    def _get_testcases_filename(self) -> str:
        if self.puzzle_file is None:
            raise ValueError("Please pass the puzzle file path when using local testcase mode")

        folder = os.path.dirname(self.puzzle_file)
        puzzle_name = os.path.splitext(os.path.basename(self.puzzle_file))[0]
        return os.path.join(folder, f"{puzzle_name}-testcases.txt")

    def _read_input_lines_from_file(self, case_nr: int) -> list[str]:
        """Read a specific test case from file and return all lines."""
        testcases_filename = self._get_testcases_filename()

        with open(testcases_filename, "r") as f:
            # Find the specific test case
            search_string = f"=== Input {case_nr} ===\n"
            for line in f:
                if search_string in line:
                    break
            else:
                raise ValueError(f"Test case {case_nr} not found")

            # Read lines until next case or end of file
            lines = []
            for next_line in f:
                if next_line.startswith("==="):  # Stop at next case
                    break
                lines.append(next_line.rstrip())

            # Remove all trailing empty lines
            while lines and not lines[-1]:
                lines.pop()

            return lines

    def _read_output_lines_from_file(self, case_nr: int) -> list[str]:
        """Read the expected output for a specific test case from file."""
        testcases_filename = self._get_testcases_filename()

        with open(testcases_filename, "r") as f:
            # Find the specific test case
            search_string = f"=== Output {case_nr} ===\n"
            for line in f:
                if search_string in line:
                    break
            else:
                raise ValueError(f"Output for test case {case_nr} not found")

            # Read lines until next case or end of file
            lines = []
            for next_line in f:
                if next_line.startswith("==="):  # Stop at next case
                    break
                lines.append(next_line.rstrip())

            # Remove all trailing empty lines
            while lines and not lines[-1]:
                lines.pop()

            return lines

    def input(self) -> str:
        """Read one line at a time, mimicking input()."""
        if self.from_web:
            return input()
        else:
            if not self.input_lines or self.line_index >= len(self.input_lines):
                raise IndexError("No more lines to read")
            line = self.input_lines[self.line_index]
            self.line_index += 1
            return line

    def add_output_line(self, line):
        """Add a line to the output buffer."""
        line = str(line)
        if self.from_web:
            print(line)
        else:
            self.actual_output_lines.append(line)

    def assert_output(self, verbose=False):
        """Assert that the actual output matches the expected output."""
        if self.from_web:
            return  # No assertion in web mode

        is_correct = self.actual_output_lines == self.expected_output_lines
        print()
        print(f"Checking test case {self.case_nr}")
        if verbose:
            print("Expected output:")
            for line in self.expected_output_lines:
                print(line)
            print("Actual output:")
            for line in self.actual_output_lines:
                print(line)
        print(f"Result: {'CORRECT' if is_correct else 'INCORRECT'}")
        print()

    def print(self, line):
        """Print the actual line and add it to the output queue so we can assert."""
        print(line)
        self.add_output_line(line)  # Add empty line to separate from previous output
