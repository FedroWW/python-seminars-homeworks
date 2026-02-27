def bfs(graph, start):
    n = len(graph)
    distance = [-1] * n  # -1 = не посещено
    parent = [-1] * n
    queue = [start]
    distance[start] = 0

    i = 0  # индекс начала очереди
    while i < len(queue):
        u = queue[i]
        i += 1  # "вытащили" u

        for v in graph[u]:
            if distance[v] == -1:  # не посещена
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)

    return distance, parent

# Наш граф (нумерация 0=A,1=B,2=C,3=D,4=E)
graph = [
    [1,2],  # A → B,C
    [0,3],  # B → A,D
    [0,3],  # C → A,D
    [1,2,4],# D → B,C,E
    [3]     # E → D
]

dist, par = bfs(graph, 0)
print("Расстояния от A:", dist)  # [0, 1, 1, 2, 3]
