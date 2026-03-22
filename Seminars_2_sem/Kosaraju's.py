def transpose(G): #транспонирование=ребра меняют направление,
    adj_dict = {} # в этом графе компоненты сильной связности не поменяются
    for v in G.keys():
        adj_dict[v] = []
    for v in G.keys():
        for u in G[v]:
            adj_dict[u].append(v)
    return adj_dict
def dfs(graph, v, visited, stack):
    visited[v] = True
    for neighbor in graph[v]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, stack)
    stack.append(v)

def Kosaraju(G):
    stack = []
    visited = [False] * len(G.keys())
    for i in range(len(G.keys())):
        if not visited[i]:
            dfs(G, i, visited, stack)
    transposed = transpose(G)
    visited = [False] * len(G.keys())
    scc = []

    while stack:
        v = stack.pop()
        if not visited[v]:
            component = []
            dfs(transposed, v, visited, component)
            scc.append(component)

    return scc

G = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [4],
    4: [5, 6],
    5: [3],
    6: [6]  # петля
}

scc = Kosaraju(G)
print(scc)  # [[0, 1, 2], [3, 4, 5], [6]]