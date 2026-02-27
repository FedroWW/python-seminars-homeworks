# Граф как словарь: ключ=вершина, значение=список соседей
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['D']
}

def euler_path(graph, start):
    # Копируем граф, чтобы не портить оригинал
    remaining_edges = {v: list(graph[v]) for v in graph}

    stack = [start]
    result = []

    while stack:
        v = stack[-1]  # Текущая вершина (последняя в стеке)

        if remaining_edges[v]:  # Есть неиспользованные рёбра
            w = remaining_edges[v].pop()  # Берём любое ребро v→w
            # Удаляем обратное ребро w→v
            if w in remaining_edges and v in remaining_edges[w]:
                remaining_edges[w].remove(v)
            stack.append(w)
        else:
            # Нет рёбер — добавляем в результат
            result.append(stack.pop())

    return result[::-1]  # Разворачиваем результат

# Запуск
path = euler_path(graph, 'E')
print('→'.join(path))  # E→D→C→A→B→D→E

#_________
#ДЛЯ ЦИКЛА
#_________

# Граф со ВСЕМИ чётными степенями (должен быть цикл)
graph_cycle = {
    'A': ['B', 'D'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['A', 'C']
}

cycle = euler_path(graph_cycle, 'A')
print('Цикл:', '→'.join(cycle))