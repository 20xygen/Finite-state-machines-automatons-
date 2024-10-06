from models.auto import Automaton, Vertex


def clear(*args: Automaton):  # makes given automaton empty (and invalid: start is None)
    for auto in args:
        auto.start = None
        auto.vertices = set()


def merge(alpha: Automaton, beta: Automaton) -> Automaton:  # makes given automaton empty
    start = Vertex(False, {'': {alpha.start, beta.start}})
    auto = Automaton(start, alpha.vertices | beta.vertices | {start})
    clear(alpha, beta)
    return auto


def concatenate(alpha: Automaton, beta: Automaton) -> Automaton:  # makes given automaton empty
    auto = Automaton(alpha.start, alpha.vertices | beta.vertices)
    for vert in alpha.vertices:
        if vert.terminal:
            vert.terminal = False
            if '' not in vert.delta.keys():
                vert.delta[''] = set()
            vert.delta[''].add(beta.start)
    clear(alpha, beta)
    return auto


def star(alpha: Automaton) -> Automaton:  # makes given automaton empty
    auto = Automaton(alpha.start, alpha.vertices)
    for vert in auto.vertices:
        if vert.terminal:
            vert.terminal = False
            if '' not in vert.delta.keys():
                vert.delta[''] = set()
            vert.delta[''].add(auto.start)
    clear(alpha)
    auto.start.terminal = True
    return auto


def plus(alpha: Automaton) -> Automaton:  # makes given automaton empty
    auto = Automaton(alpha.start, alpha.vertices)
    for vert in auto.vertices:
        if vert.terminal:
            if '' not in vert.delta.keys():
                vert.delta[''] = set()
            vert.delta[''].add(auto.start)
    clear(alpha)
    return auto
