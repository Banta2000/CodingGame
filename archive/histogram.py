import os

full_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
counter = {letter: 0 for letter in full_alphabet}


class InputReader:
    def __init__(self, case_nr=None):
        if case_nr is None:
            self.from_web = True
            self.lines = None
            self.line_index = 0
        else:
            self.from_web = False
            self.lines = self._read_case_from_file(case_nr)
            self.line_index = 0

    def _read_case_from_file(self, case_nr: int) -> list[str]:
        """Read a specific test case from file and return all lines."""
        current_file = os.path.basename(__file__)[:-3]
        testcases_filename = current_file + "-testcases.txt"

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

            # Remove empty line at the end if it exists
            if lines and not lines[-1]:
                lines.pop()

            return lines

    def input(self) -> str:
        """Read one line at a time, mimicking input()."""
        if self.from_web:
            return input()
        else:
            if not self.lines or self.line_index >= len(self.lines):
                raise IndexError("No more lines to read")
            line = self.lines[self.line_index]
            self.line_index += 1
            return line

    def has_more_lines(self) -> bool:
        """Check if there are more lines to read."""
        if self.from_web:
            return True  # Can't know in advance for web input
        return bool(self.lines and self.line_index < len(self.lines))

    def get_start_parameters(self):
        """Get the first line and convert to uppercase."""
        text = self.input().upper()
        return text


def draw_line(v1: float, v2: float) -> None:
    v1 = int(round(v1))
    v2 = int(round(v2))
    v1, v2 = min(v1, v2), max(v1, v2)

    # Both numbers are the same or v1 is zero
    if v1 == v2 == 0:
        s = "  +"
    elif v1 == v2 or v1 == 0:
        s = f"  +{'-' * v2}+"
    else:
        s = f"  +{'-' * v1}+{'-' * (v2-v1-1)}+"
    print(s)


def draw_bar(v: float, letter: str) -> None:
    v_r = int(round(v))
    if v_r == 0:
        s = f"{letter} |{v:.2f}%"
    else:
        s = f"{letter} |{' ' * v_r}|{v:.2f}%"
    print(s)


# ********************************************************


def main():
    reader = InputReader(4)
    data = reader.get_start_parameters()

    # Count letters in the text
    for letter in data:
        if letter in counter:
            counter[letter] += 1

    # Calculate percentages
    total_letters = sum(counter.values())
    if total_letters == 0:
        print("No letters found!")
        return

    percentages = {k: v / total_letters * 100 for k, v in counter.items()}

    # Draw the histogram
    draw_line(0, percentages["A"])
    for i, letter in enumerate(full_alphabet[:-1]):
        curr_value = percentages[letter]
        next_letter = full_alphabet[i + 1]
        next_value = percentages[next_letter]
        draw_bar(curr_value, letter)
        draw_line(curr_value, next_value)

    # Draw the last bar and line
    draw_bar(percentages["Z"], "Z")
    draw_line(percentages["Z"], 0)


if __name__ == "__main__":
    main()
