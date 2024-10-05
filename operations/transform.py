from models.auto import Vertex, Automaton
from typing import List, Set
from collections import deque


class Int:
    val: int

    def __init__(self, val: int):
        self.val = val


def dfs_index(counter: Int, vert: Vertex):
    if vert.index < 0:
        vert.index = counter.val
        counter.val += 1
        for array in vert.delta.values():
            for to in array:
                dfs_index(counter, to)


def sign(auto: Automaton) -> None:  # assume, Automaton is not signed
    counter = Int(0)
    dfs_index(counter, auto.start)


def design(auto: Automaton) -> None:  # operates with given automaton
    for vert in auto.vertices:
        vert.index = -1


def eps_closure(vert: Vertex, closure: Set[Vertex]) -> None:
    if vert in closure:
        return
    closure.add(vert)
    if '' in vert.delta.keys():
        diff = vert.delta[''] - closure
        if len(diff) > 0:
            closure.union(diff)
            for to in diff:
                eps_closure(to, closure)


def determinate(auto: Automaton, sigma: List[str]) -> (List, Automaton):  # given automaton will NOT be affected
    sign(auto)
    queue = deque()

    start = set()
    eps_closure(auto.start, start)
    queue.append((start, tuple(start)))
    start_vert = Vertex(False, {})
    found = {tuple(start): start_vert}  # map of sets of NFA states to DFA states
    ret = Automaton(start_vert, {start_vert})
    table = []
    while len(queue) > 0:
        cur, cur_tuple = queue.popleft()
        rows = [set() for _ in range(1 + len(sigma))]
        rows[0] = cur  # first value in line is the set of vertices
        for vert in cur:
            if vert.terminal:
                found[cur_tuple].terminal = True  # mark the DFA state as terminal if any NFA state is terminal
                break
        for i in range(len(sigma)):
            for vert in cur:
                if sigma[i] in vert.delta.keys():
                    closure = set()
                    for to in vert.delta[sigma[i]]:
                        eps_closure(to, closure)
                    rows[i + 1] |= closure
            if len(rows[i + 1]) > 0:
                tu = tuple(rows[i + 1])
                if tu not in found.keys():  # new vertice set
                    created = Vertex(False, {})
                    ret.vertices.add(created)
                    found[tu] = created
                    queue.append((rows[i + 1], tu))
                found[cur_tuple].delta[sigma[i]] = {found[tu]}
        table.append(rows)
    return table, ret


def make_complete(auto: Automaton, sigma: List[str]) -> None:  # operates with given automaton
    trash = Vertex(False, {})
    added = False
    for vert in auto.vertices:
        for sym in sigma:
            if sym not in vert.delta.keys():
                added = True
                vert.delta[sym] = {trash}
    if added:
        if auto.start.index >= 0:
            trash.index = len(auto.vertices)
        auto.vertices.add(trash)
        for sym in sigma:
            trash.delta[sym] = {trash}


def minimize(auto: Automaton, sigma: List[str]) -> (List[List], Automaton):  # given automaton will NOT be affected
    sign(auto)
    classes = [-1 for _ in range(len(auto.vertices))]  # index -> class
    quantity = 1
    for vert in auto.vertices:
        if not vert.terminal:
            quantity = 2
        classes[vert.index] = 1 if vert.terminal else 0
    tables = []  # to print
    while True:
        step = [None] * len(auto.vertices)  # will be appended into tables
        distributions = {}  # tuple(next vertices' classes) -> set(vertices with tuple as this)
                            # this tuple equals to line in current table
        for vert in auto.vertices:
            distribution = [None] * (1 + len(sigma))  # first value will be the class of current vertice
            distribution[0] = classes[vert.index]
            for i in range(len(sigma)):
                sym = sigma[i]
                if len(vert.delta[sym]) != 1:
                    raise ValueError  # if automaton is not determine
                else:
                    link = next(iter(vert.delta[sym]))  # the only next vertice
                    distribution[i + 1] = classes[link.index]
            tu = tuple(distribution)
            step[vert.index] = distribution
            if tu not in distributions.keys():
                distributions[tu] = set()
            distributions[tu].add(vert)  # defining a vertex for a class
        tables.append(step)
        new_quantity = 0
        for _, vertices in distributions.items():
            for vert in vertices:
                classes[vert.index] = new_quantity  # updating classes
            new_quantity += 1
        if new_quantity == quantity:  # stop if no new classes appeared
            break
        else:
            quantity = new_quantity
    vertices = [Vertex(False, {}) for _ in range(quantity)]  # vertices for new Automaton
    for vert in auto.vertices:
        new_vert = vertices[classes[vert.index]]
        if vert.terminal:
            new_vert.terminal = True
        if sigma[0] in new_vert.delta.keys():  # skip if this type of vertice has already benn processed
            continue
        for sym in sigma:
            to = next(iter(vert.delta[sym]))
            new_vert.delta[sym] = {vertices[classes[to.index]]}
    ret = Automaton(vertices[classes[auto.start.index]], set(vertices))
    return tables, ret


def complement(auto: Automaton) -> None:  # operates with given automaton
    for vert in auto.vertices:
        vert.terminal = not vert.terminal
