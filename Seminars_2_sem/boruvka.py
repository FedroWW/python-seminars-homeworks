#Изначально каждая вершина — отдельная компонента.
#Для каждой компоненты:
#найти минимальное ребро, ведущее к другой компоненте
#Добавить все найденные рёбра в остов
#Объединить соответствующие компоненты
#Повторять шаги 2–4, пока не останется одна компонента


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # сжатие пути
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # объединение по рангу
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1

        return True


def boruvka(n, edges):
    dsu = DSU(n)
    mst_weight = 0
    mst_edges = []
    components = n

    while components > 1:
        cheapest = [-1] * n

        # ищем минимальное исходящее ребро для каждой компоненты
        for i, (u, v, w) in enumerate(edges):
            root_u = dsu.find(u)
            root_v = dsu.find(v)

            if root_u == root_v:
                continue

            if cheapest[root_u] == -1 or edges[cheapest[root_u]][2] > w:
                cheapest[root_u] = i

            if cheapest[root_v] == -1 or edges[cheapest[root_v]][2] > w:
                cheapest[root_v] = i

        # добавляем найденные рёбра
        for i in range(n):
            if cheapest[i] != -1:
                u, v, w = edges[cheapest[i]]
                if dsu.union(u, v):
                    mst_weight += w
                    mst_edges.append((u, v, w))
                    components -= 1

    return mst_weight, mst_edges

edges = [
    (0, 1, 4),
    (0, 2, 3),
    (1, 2, 1),
    (1, 3, 2),
    (2, 3, 5)
]

weight, mst = boruvka(4, edges)

print("Вес MST:", weight)
print("Рёбра MST:", mst)