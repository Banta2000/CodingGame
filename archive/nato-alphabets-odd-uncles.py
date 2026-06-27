from typing import Any, Tuple, List
import os
import importlib.util


versions: dict[int, list[str]] = {
    0: "Authority, Bills, Capture, Destroy, Englishmen, Fractious, Galloping, High, Invariably, Juggling, Knights, Loose, Managing, Never, Owners, Play, Queen, Remarks, Support, The, Unless, Vindictive, When, Xpeditiously, Your, Zigzag".split(
        ", "
    ),
    1: "Apples, Butter, Charlie, Duff, Edward, Freddy, George, Harry, Ink, Johnnie, King, London, Monkey, Nuts, Orange, Pudding, Queenie, Robert, Sugar, Tommy, Uncle, Vinegar, Willie, Xerxes, Yellow, Zebra".split(
        ", "
    ),
    2: "Amsterdam, Baltimore, Casablanca, Denmark, Edison, Florida, Gallipoli, Havana, Italia, Jerusalem, Kilogramme, Liverpool, Madagascar, New-York, Oslo, Paris, Quebec, Roma, Santiago, Tripoli, Uppsala, Valencia, Washington, Xanthippe, Yokohama, Zurich".split(
        ", "
    ),
    3: "Alfa, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India, Juliett, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, X-ray, Yankee, Zulu".split(
        ", "
    ),
}


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        data = data.strip().split(" ")
        return data

    # Read from local file
    if start_data:
        current_file = os.path.basename(__file__)[:-3]  # Remove .py extension
        testcases_filename = current_file + "-testcases.py"  # Keep hyphens for actual filename
        testcases_module_name = current_file.replace("-", "_") + "_testcases"  # Underscores for module name
        current_dir = os.path.dirname(__file__)
        testcases_file_path = os.path.join(current_dir, testcases_filename)
        spec = importlib.util.spec_from_file_location(testcases_module_name, testcases_file_path)
        testcases = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(testcases)
        data = testcases.TEST_INPUTS[start_data]

    # Read from web
    else:
        data = input()

    return parse(data)


def find_version(word_lst: list) -> int:
    # Find the in which version the word belongs to
    for version, words in versions.items():
        for word in word_lst:
            if word not in words:
                break
        else:
            return version


# ********************************************************

data = get_start_parameters("test_10")
old_version = find_version(data)
new_version = (old_version + 1) % 4
old_version = versions[old_version]
new_version = versions[new_version]

res = []
for word in data:
    idx = old_version.index(word)
    res.append(new_version[idx])

print(" ".join(res))
