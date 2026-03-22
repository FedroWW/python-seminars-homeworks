def _read_graph_as_edges_list(n):
    edges = []
    for i in range(n):
        e=list(map(int,input().split()))
        edges.append(e)
        return edges

def _read_graph_as_matrix(n):
    M = [[0 for i in range(n)]for j in range(n)]
    for i in range(n):
        row= list(map(int,input().split()))
        M[i]=row
        return M


def read_graph_as_list(N, M):
    edges = _read_graph_as_edges_list(M)
    adj_dict = {(i + 1): [] for i in range(N)}
    for e in edges:
        adj_dict[e[0]].append(e[1])
    return adj_dict


def read_graph_as_list(N, M, oriented=True, weighted=False):
    edges = _read_graph_as_edges_list(M)
    adj_dict = {(i + 1): [] for i in range(N)}
    for e in edges:
        if not weighted:
            adj_dict[e[0]].append(e[1])
            if not oriented:
                adj_dict[e[1]].append(e[0])
        if weighted:
            adj_dict[e[0]].append((e[1], e[2]))
            if not oriented:
                adj_dict[e[1]].append((e[0], e[2]))
    return adj_dict


def read_graph_as_matrix(N, weighted=False):
    M = _read_graph_as_matrix(N)
    adj_dict = {(i + 1): [] for i in range(N)}
    for i in range(N):
        for j in range(N):
            if M[i][j]:
                if not weighted:
                    adj_dict[i + 1].append(j + 1)
                else:
                    adj_dict[i + 1].append((j + 1, M[i][j]))
    return adj_dict
