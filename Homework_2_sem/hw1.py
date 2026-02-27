
#Как, по словам деда, он добирался каждое утро в школу
def find_shortest_path(n, m, s, t, edges):
    INF = float('inf')

    # Создаем матрицы расстояний и следующей вершины
    dist = [[INF] * n for _ in range(n)]
    next_v = [[-1] * n for _ in range(n)]

    # Инициализация
    for i in range(n):
        dist[i][i] = 0
        next_v[i][i] = i

    # Заполняем ребра
    for u, v, w in edges:
        dist[u][v] = w
        next_v[u][v] = v

    # Алгоритм Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_v[i][j] = next_v[i][k]

    # Проверяем, существует ли путь
    if dist[s][t] == INF:
        return "Ne mogu naiti marshrut! :'("

    # Восстанавливаем путь
    path = [s]
    current = s
    while current != t:
        current = next_v[current][t]
        path.append(current)

    return f"{dist[s][t]}\n{' '.join(map(str, path))}"

'''
def test_gps_cases():
    tests = [
        # Тест 1:
        {
            "n": 8, "m": 8, "s": 0, "t": 7,
            "edges": [(0, 1, 600), (0, 2, 1200), (1, 3, 800), (2, 3, 400), (2, 4, 700), (3, 5, 500), (4, 5, 300),
                      (5, 7, 900)],
            "answer": "2800\n0 1 3 5 7"
        },
        # Тест 2:
        {
            "n": 4, "m": 3, "s": 0, "t": 3,
            "edges": [(0, 1, 1), (1, 2, 1), (0, 2, 10)],
            "answer": "Ne mogu naiti marshrut! :'("
        },
        # Тест 3:
        {
            "n": 4, "m": 4, "s": 0, "t": 3,
            "edges": [(0, 1, 4), (0, 3, 12), (1, 2, 3), (2, 3, 5)],
            "answer": "12\n0 3"
        },
        # Тест 4:
        {
            "n": 1, "m": 0, "s": 0, "t": 0,
            "edges": [],
            "answer": "0\n0"
        },
        # Тест 5:
        {
            "n": 3, "m": 3, "s": 0, "t": 2,
            "edges": [(0, 1, 5), (0, 2, 12), (1, 2, 3)],
            "answer": "8\n0 1 2"
        }
    ]

    for i, test in enumerate(tests, 1):
        print(f"Тест {i}:")
        result = find_shortest_path(test["n"], test["m"], test["s"], test["t"], test["edges"])
        print(f"Ожидаемый: {test['answer']}")
        print(f"Получено:  {result}")
        print("-" * 50)


# Запускаем тесты
test_gps_cases()
'''


#Дорога в Шереметьево
import heapq

def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0

    # (расстояние, вершина)
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = dist[u] + weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist


def find_min_tariffs(n, tariffs):
    INF = float('inf')

    # Преобразуем матрицу тарифов в список смежности для алгоритма Дейкстры
    graph = [[] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and tariffs[i][j] != -1:
                graph[i].append((j, tariffs[i][j]))

    # Дейкстра для каждой вершины
    result = []
    for start in range(n):
        distances = dijkstra(graph, start)
        # Заменяем inf на 999999 как в ожидаемом результате
        row = [int(d) if d != INF else 999999 for d in distances]
        result.append(row)

    return result

'''
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(str(x) if x < 999999 else '-1' for x in row))

test_cases = [
        # Тест 1:
        {
            "n": 5,
            "tariffs": [[0, 10, -1, -1, 25], [-1, 0, 15, 5, -1], [-1, -1, 0, 8, 12], [20, -1, -1, 0, 10], [-1, 30, -1, -1, 0]],
            "expected": [[0, 10, 25, 15, 25], [25, 0, 15, 5, 15], [28, 38, 0, 8, 12], [20, 30, 45, 0, 10], [55, 30, 45, 35, 0]]
        },

        # Тест 2: Полносвязный
        {
            "n": 3,
            "tariffs": [[0,5,9],[16,0,12],[7,3,0]],
            "expected": [[0,5,9],[16,0,12],[7,3,0]]
        },
        # Тест 3: Недостижимые города
        {
            "n": 4,
            "tariffs": [[0,10,-1,-1],[-1,0,20,-1],[-1,-1,0,30],[-1,-1,-1,0]],
            "expected": [[0,10,30,60],[999999,0,20,50],[999999,999999,0,30],[999999,999999,999999,0]]
        }
    ]

for i, test in enumerate(test_cases, 1):
    print(f"Тест {i}")
    print(f"n = {test['n']}")

    result = find_min_tariffs(test['n'], test['tariffs'])

    print("Результат:")
    print_matrix(result)
    print("\nОжидаемый:")
    for row in test['expected']:
        print(' '.join(str(x) if x < 999999 else '-1' for x in row))
    print("-" * 60)

'''

