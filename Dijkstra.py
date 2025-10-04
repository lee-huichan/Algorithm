# 20231516 이희찬 - Dijkstra's Algorithm

from heapq import heappush, heappop
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

Graph = Dict[int, List[Tuple[int, int]]]  # node -> list of (neighbor, weight)

def build_graph(n: int, edges: List[Tuple[int, int, int]]) -> Graph:
    g: Graph = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    # 고립 노드도 키 생성
    for i in range(1, n + 1):
        _ = g[i]
    return g

def dijkstra(g: Graph, start: int):
    INF = 10**18
    dist = {u: INF for u in g.keys()}
    prev: Dict[int, Optional[int]] = {u: None for u in g.keys()}
    dist[start] = 0

    pq: List[Tuple[int, int]] = [(0, start)]
    while pq:
        d, u = heappop(pq)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heappush(pq, (nd, v))
    return dist, prev

def reconstruct_path(prev: Dict[int, Optional[int]], target: int) -> List[int]:
    path: List[int] = []
    cur: Optional[int] = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

def pretty_print_result(start: int, dist: Dict[int, int], prev: Dict[int, Optional[int]]):
    print(f"[Dijkstra] start = {start}")
    for v in sorted(dist.keys()):
        if dist[v] >= 10**18:
            print(f" - {v}: unreachable")
        else:
            path = reconstruct_path(prev, v)
            print(f" - {v}: dist={dist[v]}, path={' -> '.join(map(str, path))}")

def main():
   
    N = 6
    edges = [
        (1, 2, 50),
        (1, 3, 45),
        (1, 4, 10),
        (4, 1, 20),
        (2, 3, 10),
        (2, 4, 15),
        (2, 5, 20),
        (4, 5, 15),
        (5, 6, 3),
        (5, 3, 15),
        (3, 5, 30),
    ]
    START = 1
    # ================================================

    g = build_graph(N, edges)
    dist, prev = dijkstra(g, START)
    pretty_print_result(START, dist, prev)

if __name__ == "__main__":
    main()
