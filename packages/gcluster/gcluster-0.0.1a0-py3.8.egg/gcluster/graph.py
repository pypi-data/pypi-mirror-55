from typing import Any, List, Set
from queue import Queue


class Graph:
    def __init__(self, nodes: List[Any]):
        self.num = len(nodes)
        self.nodes = nodes

    def describe(self):
        return self.nodes


class MatrixGraph(Graph):
    def __init__(self, nodes: List[Any]):
        super().__init__(nodes)
        self.iterations = 0
        self.adj: List[List[int]] = [
            [0 for j in range(self.num)] for i in range(self.num)]

    def iterate(self):
        self.iterations += 1

    def add_edge(self, a: int, b: int):
        self.adj[a][b] += 1
        self.adj[b][a] += 1

    def batch(self, iterations: int, adj: List[List[Any]]):
        self.iterations += iterations
        self.adj = [[self.adj[i][j] + adj[i][j]
                     for j in range(self.num)] for i in range(self.num)]

    def reset(self):
        self.iterations = 0
        self.adj = [[0 for j in range(self.num)] for i in range(self.num)]

    def to_list_graph(self, threshold: float = 1):
        assert self.iterations >= 1, 'No iterations yet!'
        assert 0 <= threshold <= 1, 'Invalid threshold!'
        list_graph = ListGraph(self.nodes)
        for i in range(self.num):
            for j in range(i + 1, self.num):
                if self.adj[i][j] / self.iterations >= threshold:
                    list_graph.add_edge(i, j)
        return list_graph


class ListGraph(Graph):
    def __init__(self, nodes: List[Any]):
        super().__init__(nodes)
        self.adj: List[Set[int]] = [set() for j in range(self.num)]

    def add_edge(self, a: int, b: int):
        self.adj[a].add(b)
        self.adj[b].add(a)

    def cc(self) -> List[List[Any]]:
        visited = [False for i in range(self.num)]
        ans = []
        for i in range(self.num):
            if not visited[i]:
                visited[i] = True
                ans.append([])
                queue = Queue()
                queue.put(i)

                while not queue.empty():
                    front = queue.get()
                    ans[-1].append(self.nodes[front])
                    for j in self.adj[front]:
                        if not visited[j]:
                            queue.put(j)
                            visited[j] = True

        return ans
