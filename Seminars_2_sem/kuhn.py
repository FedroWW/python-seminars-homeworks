def kuhn(graph):
    n = len(graph.keys())
    match = [-1] * n
    visited = [False] * n
    _, parts = bipartite(graph)
    L = parts[0]
    def dfs(v):
        for u in graph[v]:
            if not visited[u]:
                visited[u] = True
                if match[u] == -1 or dfs(match[u]):
                    match[u] = v
                    return True
        return False

    max_matching = 0
    for v in L:
        visited = [False] * n
        if dfs(v):
            max_matching += 1
    return max_matching