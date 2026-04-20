
def z_function(s):
    n = len(s)
    zf = [0] * n
    left, right = 0, 0
    for i in range(1, n):
        zf[i] = max(0, min(right - i, zf[i - left]))
        while i + zf[i] < n and s[zf[i]] == s[i + zf[i]]:
            zf[i] += 1
        if i + zf[i] > right:
            left = i
            right = i + zf[i]
    return zf

def prefix_function(s):
    n = len(s)
    p = [0] * n
    for i in range(1, len(s)):
        k = p[i - 1]
        while k > 0 and s[k] != s[i]:
            k = p[k - 1]
        if s[k] == s[i]:
            k += 1
        p[i] = k
    return p

class Node:
    def __init__(self):
        self.son = {} # Дочерние узлы (ключ: индекс символа)
        self.go = {} # Переходы
        self.parent = None # Родительский узел
        self.suffLink = None # Суффиксная ссылка
        self.up = None # Сжатая суффиксная ссылка
        self.charToParent = None # Символ, ведущий к родителю (индекс)
        self.isLeaf = False # Является ли узел терминальным
        self.is_root = False # Флаг корневого узла

    def get_suff_link(self):
        if self.suffLink is not None:
            return self.suffLink
        if self.is_root:
            self.suffLink = self
            return self
        if self.parent.is_root:
            self.suffLink = self.parent
            return self.suffLink
        self.suffLink = self.parent.get_suff_link().get_go(self.charToParent)
        return self.suffLink

    def get_go(self, c):
        if c in self.go:
            return self.go[c]
        if c in self.son:
            self.go[c] = self.son[c]
        elif self.is_root:
            self.go[c] = self
        else:
            self.go[c] = self.get_suff_link().get_go(c)
        return self.go[c]

    def get_up(self):
        if self.up is not None:
            return self.up
        suff_link = self.get_suff_link()
        if suff_link.isLeaf:
            self.up = suff_link
        elif suff_link.is_root:
            self.up = suff_link
        else:
            self.up = suff_link.get_up()
        return self.up

# Создание корневого узла
root = Node()
root.is_root = True
root.suffLink = root
root.up = root

def add_string(s):
    cur = root
    for char in s:
        c = ord(char) - ord('a') #номер буквы в алфавите
        if c not in cur.son:
            new_node = Node()
            new_node.parent = cur
            new_node.charToParent = c
            cur.son[c] = new_node
        cur = cur.son[c]
    cur.isLeaf = True

def process_text(t):
    cur = root
    found_patterns = []
    for i in range(len(t)):
        char = t[i]
        c = ord(char) - ord('a')
        cur = cur.get_go(c)
        node = cur
        while not node.is_root:
            if node.isLeaf:
                found_patterns.append(i)
            node = node.get_up()
    return found_patterns