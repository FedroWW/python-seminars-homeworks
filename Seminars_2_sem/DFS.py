#DFS — для глубокого исследования и задач,
# где важен порядок завершения вершин (топосорт, циклы, компоненты).
#__________________________________________________________________

def dfs(graph, start):
    visited = [False] * len(graph)
    stack = [start]

    while stack:
        u = stack.pop()  # LIFO!
        if not visited[u]:
            visited[u] = True
            print(f"Посещаем {u}")
            # Добавляем соседей в обратном порядке (важно!)
            for v in reversed(graph[u]):
                if not visited[v]:
                    stack.append(v)

graph = [
    [1,2],  # A → B,C
    [0,3],  # B → A,D
    [0,3],  # C → A,D
    [1,2,4],# D → B,C,E
    [3]     # E → D
]

dfs(graph, 0)
#__________________
#РЕКУРЕНТНАЯ ВЕРСИЯ
#-------------------

def dfs_recursive(graph, u, visited):
    visited[u] = True
    print(f"Посещаем {u}")

    for v in graph[u]:
        if not visited[v]:
            dfs_recursive(graph, v, visited)

# Запуск
graph = [[1,2], [0,3], [0], [1,4], [3]]
visited = [False] * 5
dfs_recursive(graph, 0, visited)

#____________________________
#КОД С ВОССТАНОВЛЕНИЕМ ПУТИ
#____________________________

def dfs_path(graph, start, goal, visited=None, parent=None):
    if visited is None:
        visited = [False] * len(graph)
        parent = [-1] * len(graph)

    visited[start] = True

    if start == goal:
        return True

    for v in graph[start]:
        if not visited[v]:
            parent[v] = start
            if dfs_path(graph, v, goal, visited, parent):
                return True
    return False

# Нахождение пути 0 → 4
graph = [[1,2], [0,3], [0], [1,4], [3]]
visited = [False] * 5
parent = [-1] * 5

if dfs_path(graph, 0, 4, visited, parent):
    # Восстанавливаем путь
    path = []
    v = 4
    while v != -1:
        path.append(v)
        v = parent[v]
    path.reverse()
    print("Путь:", path)  # [0, 1, 3, 4]

_______________
#РАСКРАСКА
_______________

color = ['white' for i in graph.keys()]
def dfs_visit(graph, v):
    color[v] = 'gray'
    print(v)

    for u in graph[v]:
        if color[u] == 'gray':
            print('has cycle')
        if color[u] == 'white':
            dfs_visit(graph, u)

    color[v] = 'black'

def dfs_stack(graph, start):
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            print(u)
            for i in range(len(graph[u])):
                stack.append(graph[u][i])
 
