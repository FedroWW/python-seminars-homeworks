#находим вершину в которую ничего не входит,
#потом удаляем ее и дальше опять находим вершину...
#не уникальная сортировка
#__________________________
#ЧЕРЕЗ DFS=АЛГОРИТМ ТАРЬЯНА
#__________________________
def TopSort(G):
    color = [''] + ['white' for i in G.keys()]
    topsorted = []

    def dfs_visit(graph, v):
        nonlocal topsorted
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


test_graph = {
    1: [2, 3],
    2: [4],
    3: [4],
    4: []
}

print(TopSort(test_graph))
#______________
#ЧЕРЕЗ ОЧЕРЕДЬ=АЛГОРИТМ КАНА
#______________
def topological_sort_kahn(graph):
    n = len(graph)
    in_degree = [0] * n

    # 1. ТОЧНЫЙ подсчёт входящих
    for u in range(n):
        for v in graph[u]:
            in_degree[v] += 1  # Все рёбра учтены

    print(f"in_degree: {in_degree}")

    # 2. Начальная очередь
    queue = [i for i in range(n) if in_degree[i] == 0]
    print(f"Очередь: {queue}")

    order = []

    while queue:
        u = queue.pop(0)
        order.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # 3. ПРОВЕРКА цикла
    if len(order) == n:
        return order
    else:
        return None, f"Цикл! Обработано {len(order)}/{n} вершин"

# Тест
graph = [[1], [3,4], [], [], []]
result = topological_sort_kahn(graph)
print("Результат:", result)
