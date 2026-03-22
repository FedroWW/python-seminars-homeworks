def connected_components(graph):
    visited = set()
    components = []

    vertices = list(range(len(graph))) #граф задан списком смежности

    for start in vertices:
        if start in visited:
            continue

        # Новая компонента
        comp = []
        stack = [start]
        visited.add(start)

        while stack:
            u = stack.pop()
            comp.append(u)

            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    stack.append(v)

        components.append(comp)

    return components #список списков, где каждый внутренний список
                      # — вершины одной компоненты связности

# Граф: 0-1, 2-3, 4 изолирована
graph = [
    [1],     # вершина 0 связана с 1
    [0],     # вершина 1 связана с 0
    [3],     # вершина 2 связана с 3
    [2],     # вершина 3 связана с 2
    []       # вершина 4 изолирована
]

result = connected_components(graph)
print(result)  # [[0, 1], [2, 3], [4]]

