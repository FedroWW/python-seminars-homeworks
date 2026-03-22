class DSU:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x):
        # эвристика сжатия путей
        if self.parent[x] != x:  # если parent это не корень
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:  # если они в разных множествах
            if self.rank[rootX] > self.rank[rootY]:  # ранговая эвристика
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def TopSort(G):
    color = [''] + ['white' for i in G.keys()]
    topsorted = []

    def dfs_visit(graph, v):
        global topsorted
        color[v] = 'gray'
        print(v)

        for u in graph[v]:
            if color[u] == 'gray':
                print('has cycle')
            if color[u] == 'white':
                dfs_visit(graph, u)

        color[v] = 'black'
        topsorted.append(v)

    for i in range(len(color)):
        if color[i] == 'white':
            dfs_visit(G, i)

    return topsorted[::-1]


# Создаём DSU для 5 элементов
dsu = DSU(5)

# Объединяем пары
dsu.union(0, 1)  # {0, 1}
dsu.union(2, 3)  # {2, 3}
dsu.union(0, 2)  # {0, 1, 2, 3}

# Проверяем связи
print(dsu.connected(1, 3))  # True — в одном множестве
print(dsu.connected(1, 4))  # False — 4 изолирована

# Состояние после объединений:
# parent: [0, 0, 0, 0, 4] (примерно)
# rank:   [2, 1, 1, 1, 1]