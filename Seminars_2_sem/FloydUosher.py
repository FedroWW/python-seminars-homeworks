#Во взвешенном графе нахождение длин кратчайших путей
# между всевозможными парами вершин с помощью дпшки
#----------------------------------------------------

def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]  # копия матрицы

    # Для каждой промежуточной вершины k
    for k in range(n):
        print(f"Через вершину {k}:")
        for i in range(n):
            for j in range(n):
                # Путь через k лучше прямого?
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    print(f"  {i}→{j}: {dist[i][j]} через {k}")

    return dist

INF = float('inf')
graph = [
    [0, 4, INF, 5, INF],
    [INF, 0, 1, INF, 6],
    [2, INF, 0, 3, INF],
    [INF, INF, 1, 0, 2],
    [1, INF, INF, 4, 0]
]

result = floyd_warshall(graph)
print("Финальные расстояния:")
for i in range(len(result)):
    print(f"{i}: {result[i]}")
