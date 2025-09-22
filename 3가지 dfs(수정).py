from collections import defaultdict, deque
import os

# [1] 그래프 로딩 + 중복 제거 + 이웃 정렬
def load_graph(path='searchgraph.txt'):
    raw = defaultdict(set)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                u, v = map(int, line.split())
                raw[u].add(v)
                raw[v].add(u)  # 무방향
    # set -> sorted list
    graph = {u: sorted(neis) for u, neis in raw.items()}
    return graph

# (1) 재귀 DFS
def dfs_recursive_util(u, visited, graph, order):
    visited[u] = True
    order.append(u)
    for w in graph.get(u, []):
        if not visited[w]:
            dfs_recursive_util(w, visited, graph, order)

def dfs_recursive_all(graph):
    visited = {u: False for u in graph}
    orders = []
    for s in sorted(graph):  # 낮은 번호부터 컴포넌트 순회
        if not visited[s]:
            comp = []
            dfs_recursive_util(s, visited, graph, comp)
            orders.append(comp)
    return orders

# (2) 스택 DFS (visit 확인 후 push)
def dfs_stack1_component(start, graph, visited):
    order = []
    stack = [start]
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        # 인접 리스트를 오름차순으로 정렬해두었으니
        # 낮은 번호 우선 방문을 원하면 push는 역순
        for w in reversed(graph.get(u, [])):
            if not visited[w]:
                stack.append(w)
    return order

def dfs_stack1_all(graph):
    visited = {u: False for u in graph}
    orders = []
    for s in sorted(graph):
        if not visited[s]:
            orders.append(dfs_stack1_component(s, graph, visited))
    return orders

# (3) 스택 + can_explore/next_cell (미로 스타일)
def dfs_stack2_component(start, graph, visited):
    order = []
    idx_map = {u: 0 for u in graph}
    stack = [start]
    u = start
    while stack:
        if not visited[u]:
            visited[u] = True
            order.append(u)

        # 현재 u에서 아직 안 간 이웃이 있는지
        def can_explore(u):
            i = idx_map[u]
            while i < len(graph.get(u, [])) and visited[graph[u][i]]:
                i += 1
            idx_map[u] = i
            return i < len(graph.get(u, []))

        if can_explore(u):
            v = graph[u][idx_map[u]]
            idx_map[u] += 1
            stack.append(u)
            u = v
        else:
            # 더 갈 곳 없으면 되돌아감
            stack.pop()
            if stack:
                u = stack[-1]
    return order

def dfs_stack2_all(graph):
    visited = {u: False for u in graph}
    orders = []
    for s in sorted(graph):
        if not visited[s]:
            orders.append(dfs_stack2_component(s, graph, visited))
    return orders

# Main Code
if __name__ == "__main__":
    graph = load_graph('searchgraph.txt')
    
    rec = dfs_recursive_all(graph)
    it1 = dfs_stack1_all(graph)
    it2 = dfs_stack2_all(graph)

    print("dfs1 (재귀, 컴포넌트별):", rec)
    print("dfs2 (스택, 컴포넌트별):", it1)
    print("dfs3 (스택-미로, 컴포넌트별):", it2)
