#КЛАССИЧЕСКАЯ ВЕРСИЯ
#-------------------

def dijkstra_simple(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    used = [False] * n

    for _ in range(n):
        # Найти ближайшую
        u = -1
        min_d = float('inf')
        for i in range(n):
            if not used[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i

        if u == -1: break
        used[u] = True

        # Обновить соседей
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return dist

# Тест
graph = [[(1,7),(2,5),(3,3)], [(2,1),(4,2)], [(4,3)], [(2,2)], []]
print(dijkstra_simple(graph, 0))  # [0, 8, 5, 3, 6]

#_____________
#ЧЕРЕЗ КУЧУ
#_____________

import heapq

def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0

    # (расстояние, вершина)
    pq = [(0, start)]

    print(f"Поиск от вершины {start}")
    print("Шаг | dist | очередь | обновления")
    print("-" * 40)

    step = 0
    while pq:
        d, u = heapq.heappop(pq)
        step += 1

        if d > dist[u]:
            continue

        print(f"{step:2} | {dist} | pq: {pq} | взяли {u}(d={d})")

        for v, weight in graph[u]:
            old_dist = dist[v]
            new_dist = dist[u] + weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
                print(f"    → {v}: {old_dist} → {new_dist}")

    return dist

# списки смежности [(сосед, вес), ...]
graph = [
    [(1, 7), (2, 5), (3, 3)],  # из 0
    [(2, 1), (4, 2)],          # из 1
    [(4, 3)],                  # из 2
    [(2, 2)],                  # из 3
    []                         # из 4
]

distances = dijkstra(graph, 0)
print(f"Кратчайшие расстояния от 0: {distances}")

#_______________________
#С ВОССТАНОВЛЕНИЕМ ПУТИ
#-----------------------

def Dijkstra(G,s):
    V = len(G.keys()) + 1
    dist = [float('inf') for i in range(V)]
    prev = [None for i in range(V)]
    dist[s] = 0
    S = set()
    S.add(0)
    while len(S) < V:
        v = dist.index(min(dist)) # можно поменять на кучу
        S.add(v)
        for u, w in G[v]:
            if u not in S and dist[u] > dist[v] + w:
                prev[u] = v
                dist[u] = dist[v] + w
        dist[v] = float('inf')

    print(prev) # получаем кратчайшие пути, можно по ним восстановить стоимости
