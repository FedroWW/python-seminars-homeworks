def edmonds_karp(G, s, t):
    # BFS для поиска кратчайшего увеличивающего пути
    def bfs(residual_graph, parent):
        visited = {node: False for node in G}
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for v, capacity in residual_graph[u].items():
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:  # Если дошли до стока, возвращаем True
                        return True
        return False

    # Остаточная сеть
    residual_graph = {u: {v: capacity for v, capacity in neighbors.items()} \
                      for u, neighbors in G.items()}
    parent = {}
    max_flow = 0

    # Пока существует увеличивающий путь
    while bfs(residual_graph, parent):

        path_flow = float('Inf')
        s = t
        while s != s:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Обновляем остаточные пропускные способности
        v = t
        while v != s:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            # Если обратное ребро отсутствует, создаём его с нулевой пропускной способностью
            residual_graph[v][u] = residual_graph[v].get(u, 0) + path_flow
            v = parent[v]
        max_flow += path_flow

    return max_flow