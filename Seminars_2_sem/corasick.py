from collections import deque


class Node:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []  # список шаблонов, которые заканчиваются в этом узле


class AhoCorasick:
    def __init__(self, patterns):
        self.root = Node()
        self._build_trie(patterns)
        self._build_fail_links()

    def _build_trie(self, patterns):
        for pattern in patterns:
            node = self.root
            for char in pattern:
                node = node.children.setdefault(char, Node())
            node.output.append(pattern)

    def _build_fail_links(self):
        queue = deque()

        # 1. Для детей корня fail = root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        # 2. BFS
        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                fail_node = current.fail

                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail

                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self.root
                child.output += child.fail.output

                queue.append(child)

    def search(self, text):
        node = self.root
        results = []

        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail

            node = node.children[char] if node and char in node.children else self.root

            for pattern in node.output:
                results.append((i - len(pattern) + 1, pattern))

        return results


patterns = ["he", "she", "his", "hers"]
text = "ushers"

ac = AhoCorasick(patterns)
matches = ac.search("ushers")
print(matches)
