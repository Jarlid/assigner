from random import shuffle


def get_flow(graph: list[list[int]], source: int, sink: int) -> (int, list[list[int]]):
    graph_size = len(graph)

    for row in graph:
        if len(row) != graph_size:
            raise ValueError("Graph must be a square table.")

    def bfs(start: int, end: int, parent: list[int]):
        visited = [False] * graph_size
        visited[start] = True

        queue = [start]
        while queue:
            v = queue.pop(0)

            us = list(range(len(graph[v])))
            shuffle(us)

            for u in us:
                if graph[v][u] > 0 and visited[u] is False:
                    queue.append(u)
                    visited[u] = True
                    parent[u] = v
                    if u == end:
                        return True

        return False

    def ford_fulkerson(start: int, end: int):
        parent = [-1] * graph_size
        max_flow = 0

        while bfs(start, end, parent):

            curr_flow = float("Inf")
            v = end
            while v != start:
                curr_flow = min(curr_flow, graph[parent[v]][v])
                v = parent[v]

            max_flow += curr_flow

            v = end
            while v != start:
                graph[parent[v]][v] -= curr_flow
                graph[v][parent[v]] += curr_flow
                v = parent[v]

        return max_flow

    return ford_fulkerson(source, sink), graph
