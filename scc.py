import sys
sys.setrecursionlimit(10**7)

def read_graph(path):
    
    n = m = None
    edges = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            if n is None:
                parts = s.split()
                n, m = map(int, parts[:2])
            else:
                u, v = map(int, s.split()[:2])
                edges.append((u, v))
    if n is None:
        raise ValueError("첫 줄에 n m 이 있어야 합니다.")
    # 0/1 인덱스 자동 보정
    if edges:
        mn = min(min(u, v) for (u, v) in edges)
        off = 1 if mn == 1 else 0
        edges = [(u - off, v - off) for (u, v) in edges]
    g = [[] for _ in range(n)]
    gt = [[] for _ in range(n)]
    for (u, v) in edges:
        g[u].append(v)
        gt[v].append(u)
    return n, g, gt

def kosaraju(n, g, gt):
    """코사라주 2단계 DFS"""
    visited = [False]*n
    order = []

    def dfs1(v):
        visited[v] = True
        for u in g[v]:
            if not visited[u]:
                dfs1(u)
        order.append(v)

    for v in range(n):
        if not visited[v]:
            dfs1(v)

    comp_id = [-1]*n
    comps = []

    def dfs2(v, cid):
        comp_id[v] = cid
        comps[cid].append(v)
        for u in gt[v]:
            if comp_id[u] == -1:
                dfs2(u, cid)

    order.reverse()
    cid = 0
    for v in order:
        if comp_id[v] == -1:
            comps.append([])
            dfs2(v, cid)
            cid += 1

    # 안정적 출력을 위해 각 컴포넌트 정렬
    for comp in comps:
        comp.sort()
    return comp_id, comps

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "searchgraph.txt"
    n, g, gt = read_graph(path)
    comp_id, comps = kosaraju(n, g, gt)
    print(f"# of nodes: {n}")
    print(f"# of SCCs: {len(comps)}")
    for i, c in enumerate(comps):
        print(f"SCC {i}: size={len(c)} nodes={[x+1 for x in c]}")
