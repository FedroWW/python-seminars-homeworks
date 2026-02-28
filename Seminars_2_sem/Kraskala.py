def kruskal(graph_edges, n):
    """
    graph_edges: list[(w, u, v)]
    """
    # Сортируем рёбра
    graph_edges.sort()
    #print(graph_edges)

    # Изначально каждый = своей компоненте
    component = list(range(n))  # component[i] = группа i

    mst_edges = []
    mst_weight = 0

    def same_component(u, v):
        """В одной компоненте?"""
        return component[u] == component[v]

    def merge_components(u, v):
        """Объединить компоненты"""
        cu, cv = component[u], component[v]
        if cu != cv:
            # Меняем всю группу cv на cu
            for i in range(n):
                if component[i] == cv:
                    component[i] = cu
            return True
        return False

    # Добавляем рёбра по весу
    for w, u, v in graph_edges:
        if not same_component(u, v):  # не цикл?
            if merge_components(u, v):
                mst_edges.append((w, u, v))
                mst_weight += w

    return mst_edges, mst_weight

# Тест
graph_edges = [
    (1, 0, 2), (3, 0, 1), (2, 1, 3), (5, 1, 3),
    (2, 2, 4), (3, 2, 5), (1, 4, 6)
]

n = 7
mst_edges, weight = kruskal(graph_edges, n)
print(f"MST вес: {weight}")
print("Рёбра:", mst_edges)