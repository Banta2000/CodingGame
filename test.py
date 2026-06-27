from itertools import combinations


BP = [
    {"fromNode": "0", "toNode": "24"},
    {"fromNode": "1", "toNode": "26"},
    {"fromNode": "2", "toNode": "20"},
    {"fromNode": "3", "toNode": "12"},
    {"fromNode": "4", "toNode": "13"},
    {"fromNode": "5", "toNode": "14"},
    {"fromNode": "6", "toNode": "15"},
    {"fromNode": "7", "toNode": "16"},
    {"fromNode": "8", "toNode": "17"},
    {"fromNode": "9", "toNode": "18"},
    {"fromNode": "10", "toNode": "19"},
    {"fromNode": "11", "toNode": "29"},
    {"fromNode": "12", "toNode": "20"},
    {"fromNode": "13", "toNode": "12"},
    {"fromNode": "13", "toNode": "14"},
    {"fromNode": "14", "toNode": "21"},
    {"fromNode": "15", "toNode": "14"},
    {"fromNode": "15", "toNode": "16"},
    {"fromNode": "16", "toNode": "22"},
    {"fromNode": "17", "toNode": "23"},
    {"fromNode": "18", "toNode": "17"},
    {"fromNode": "18", "toNode": "19"},
    {"fromNode": "19", "toNode": "28"},
    {"fromNode": "20", "toNode": "21"},
    {"fromNode": "21", "toNode": "27"},
    {"fromNode": "22", "toNode": "21"},
    {"fromNode": "22", "toNode": "23"},
    {"fromNode": "23", "toNode": "33"},
    {"fromNode": "24", "toNode": "25"},
    {"fromNode": "24", "toNode": "37"},
    {"fromNode": "25", "toNode": "30"},
    {"fromNode": "26", "toNode": "25"},
    {"fromNode": "26", "toNode": "27"},
    {"fromNode": "27", "toNode": "31"},
    {"fromNode": "28", "toNode": "35"},
    {"fromNode": "29", "toNode": "28"},
    {"fromNode": "29", "toNode": "36"},
    {"fromNode": "30", "toNode": "38"},
    {"fromNode": "31", "toNode": "30"},
    {"fromNode": "31", "toNode": "32"},
    {"fromNode": "32", "toNode": "39"},
    {"fromNode": "33", "toNode": "32"},
    {"fromNode": "33", "toNode": "34"},
    {"fromNode": "34", "toNode": "41"},
    {"fromNode": "35", "toNode": "34"},
    {"fromNode": "35", "toNode": "36"},
    {"fromNode": "36", "toNode": "41"},
    {"fromNode": "37", "toNode": "A"},
    {"fromNode": "38", "toNode": "37"},
    {"fromNode": "38", "toNode": "39"},
    {"fromNode": "39", "toNode": "40"},
    {"fromNode": "40", "toNode": "B"},
    {"fromNode": "40", "toNode": "43"},
    {"fromNode": "41", "toNode": "42"},
    {"fromNode": "42", "toNode": "44"},
    {"fromNode": "42", "toNode": "45"},
    {"fromNode": "43", "toNode": "C"},
    {"fromNode": "44", "toNode": "43"},
    {"fromNode": "44", "toNode": "45"},
    {"fromNode": "45", "toNode": "D"},
]


def get_val(node_id, MP, outgoing_counts, init_config):
    if node_id in init_config:
        return init_config[node_id]
    else:
        return sum(
            get_val(from_node, MP, outgoing_counts, init_config) / outgoing_counts[from_node]
            for from_node in MP[node_id]
        )


def try_solution(conf):
    init_config = {}
    for i, val in enumerate(conf):
        init_config[str(i)] = val

    MP = {}
    outgoing_counts = {}
    for edge in BP:
        from_node = edge["fromNode"]
        to_node = edge["toNode"]
        if to_node not in MP:
            MP[to_node] = []
        MP[to_node].append(from_node)
        outgoing_counts[from_node] = outgoing_counts.get(from_node, 0) + 1

    A = get_val("A", MP, outgoing_counts, init_config)
    B = get_val("B", MP, outgoing_counts, init_config)
    C = get_val("C", MP, outgoing_counts, init_config)
    D = get_val("D", MP, outgoing_counts, init_config)

    if [A, B, C, D] == [8, 8, 10, 6]:
        print("Success!", conf)
        return True

    return False


def iter_confs(length=12, four_count=8):
    for four_positions in combinations(range(length), four_count):
        conf = [0] * length
        for pos in four_positions:
            conf[pos] = 4
        yield conf


matches = 0
checked = 0

for conf in iter_confs():
    checked += 1
    if try_solution(conf):
        matches += 1

print(f"Checked {checked} unique permutations, found {matches} matches.")


conf = [4, 4, 4, 4, 0, 4, 0, 4, 0, 4, 0, 4]
