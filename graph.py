from collections import deque
from bitarray import bitarray


class BiGraph(object):
    def __init__(self, n):
        self._nodes = [[] for _ in range(n)]
        self._n_bonds = 0

    def clear(self):
        for n in self._nodes:
            n.clear()
        self._n_bonds = 0

    def neighbours(self, i: int):
        return self._nodes[i]

    def __len__(self):
        return len(self._nodes)

    def n_bonds(self):
        return self._n_bonds

    def bonded(self, i, j):
        return j in self._nodes[i] and i in self._nodes[j]

    def bond(self, i, j):
        if not self.bonded(i, j):
            self._nodes[i].append(j)
            self._nodes[j].append(i)
            self._n_bonds += 1
            return
        print(f"[warn] repeated bond with ({i}, {j})")


class DiGraph(object):
    def __init__(self, n):
        self._nodes = [[] for _ in range(n)]
        self._n_bonds = 0

    def clear(self):
        for n in self._nodes:
            n.clear()
        self._n_bonds = 0

    def __len__(self):
        return len(self._nodes)

    def n_bonds(self):
        return self._n_bonds

    def bond(self, i, j):
        i_already_in_j = j in self._nodes[i]
        if not i_already_in_j:
            self._nodes[i].append(j)
            self._n_bonds += 1
            return
        print(f"[warn] repeated bond with ({i}, {j})")


def bfs(bg: BiGraph, start: int):
    qu = deque()
    qu.append(start)
    seen = {start}
    while qu:
        e = qu.popleft()
        ns = bg.neighbours(e)
        for n in ns:
            if n not in seen:
                qu.append(n)
                seen.add(n)
    return list(seen)


def all_connected_components(bg: BiGraph):
    seen = bitarray(len(bg))
    result = []
    for i in range(len(bg)):
        if not seen[i]:
            if not bg.neighbours(i):
                seen[i] = True
                continue
            lst = bfs(bg, i)
            result.append(lst)
            for e in lst:
                seen[e] = True
    return result


if __name__ == '__main__':
    bg = BiGraph(8)
    bg.bond(1, 3)
    print(bg.bonded(1, 3))
    print(bg.n_bonds())
