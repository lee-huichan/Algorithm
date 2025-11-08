# 202315167 컴퓨터과학전공 이희찬
# Week 10 - PE05 Kruskal Algorithm

from typing import List, Tuple, Dict

class UnionFind:
    def __init__(self, vertices: List[str]):
        self.parent: Dict[str, str] = {v: v for v in vertices}
        self.rank: Dict[str, int] = {v: 0 for v in vertices}

    def find(self, x: str) -> str:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

def kruskal(vertices: List[str], edges: List[Tuple[str, str, int]]):
    edges_sorted = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(vertices)
    mst = []
    total = 0

    for u, v, w in edges_sorted:
        if uf.unite(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == len(vertices) - 1:
                break
    return mst, total

def main():
    # 정점: A, B, C, D, E
    vertices = ["A", "B", "C", "D", "E"]

    # 그림에 표시된 간선/가중치 (무방향 그래프)
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 2),
        ("C", "D", 4),
        ("B", "E", 3),
        ("D", "E", 1),
        ("C", "E", 5),
    ]

    mst, total = kruskal(vertices, edges)

    print("----- Kruskal MST 결과 -----")
    for u, v, w in mst:
        print(f"{u} - {v} (w={w})")
    print(f"총 가중치: {total}")

if __name__ == "__main__":
    main()
