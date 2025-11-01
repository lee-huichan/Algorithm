import heapq

class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

def build_huffman_tree(freqs):
    # freqs: dict[symbol] = frequency(int)
    # 힙에는 (freq, uid, node)를 넣어서 동률일 때도 안정적으로 동작
    heap = []
    uid = 0
    for s, f in freqs.items():
        heapq.heappush(heap, (f, uid, Node(f, symbol=s)))
        uid += 1

    # 심볼이 하나인 경우 처리
    if len(heap) == 1:
        f, _, only = heap[0]
        return Node(f, left=only, right=None)

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        parent = Node(f1 + f2, left=n1, right=n2)
        heapq.heappush(heap, (parent.freq, uid, parent))
        uid += 1
    return heap[0][2]

def build_codes(root):
    codes = {}
    def dfs(node, path):
        if node is None:
            return
        if node.is_leaf():
            # 단일 심볼 트리인 경우 빈 문자열 방지
            codes[node.symbol] = path if path != '' else '0'
            return
        dfs(node.left, path + '0')
        dfs(node.right, path + '1')
    dfs(root, '')
    return codes

def main():
    # 과제 표의 probability (영문 빈도) → ×10000 정수화
    prob = {
        'A': 0.08833, 'B': 0.01267, 'C': 0.02081, 'D': 0.04376, 'E': 0.14878,
        'F': 0.02455, 'G': 0.01521, 'H': 0.05831, 'I': 0.05644, 'J': 0.00880,
        'K': 0.00867, 'L': 0.04124, 'M': 0.02361, 'N': 0.06498, 'O': 0.07245,
        'P': 0.02575, 'Q': 0.00880, 'R': 0.06872, 'S': 0.05537, 'T': 0.09351,
        'U': 0.02762, 'V': 0.01160, 'W': 0.01868, 'X': 0.00146, 'Y': 0.01521, 'Z': 0.00053
    }
    freqs = {}
    for s, p in prob.items():
        cnt = int(round(p * 10000))
        if cnt <= 0:
            cnt = 1
        freqs[s] = cnt

    root = build_huffman_tree(freqs)
    codes = build_codes(root)

    # 출력: 심볼 알파벳 순으로, 빈도와 코드
    print("=== Huffman Codes (alphabetical) ===")
    for s in sorted(freqs.keys()):
        print(f"{s}: freq={freqs[s]}, code={codes[s]}")

    total = sum(freqs.values())
    avg_len = 0.0
    for s, f in freqs.items():
        avg_len += (f / total) * len(codes[s])
    print("\nAverage code length: {:.4f} bits/symbol".format(avg_len))

if __name__ == "__main__":
    main()
