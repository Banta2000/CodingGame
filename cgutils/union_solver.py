class UnionSolver:
    def __init__(self, items):
        self.items = items
        self.roots = {item: item for item in items}

    def add_edge(self, edge: tuple):
        # Adds an edge to the union, connecting two items (making rootA the root of B), returning True
        # Returns False if the two items are already in the same union
        a, b = edge
        if a not in self.items:
            print(f"Error: {a} not in items")
        if b not in self.items:
            print(f"Error: {b} not in items")
        root_a = self.find_root(a)
        root_b = self.find_root(b)
        if root_a != root_b:
            self.roots[root_b] = root_a
            return True
        return False

    def find_root(self, item):
        # Returns the ultimate root of the item
        if item not in self.roots:
            print(f"Error: {item} not in roots")
            return None

        while self.roots[item] != item:
            item = self.roots[item]
        return item

    def compress(self):
        # Compress the path to the root for the item; update the ultimate root for each item
        for item in self.roots:
            self.roots[item] = self.find_root(item)

    def get_unions(self):
        # Returns a list of sets; each set contains items that are in the same union
        self.compress()
        unions = {}
        for item in self.roots:
            root = self.roots[item]
            if root not in unions:
                unions[root] = set()
            unions[root].add(item)
        return list(unions.values())
