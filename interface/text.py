from models.auto import Automaton, Vertex
from operations.transform import sign


def str_to_nfa(text: str) -> Automaton:
    lines = text.split('\n')
    indexes = []
    fins = []
    for line in lines:
        pos = line.find(':')
        if pos >= 0:
            if line[:pos] == 'F':
                if len(line) > 2:
                    fins = list(map(int, line[pos + 2:].split()))
            else:
                indexes.append(int(line[:pos]))
    vertices = {index: Vertex(False, {}, index) for index in indexes}
    for fin in fins:
        vertices[fin].terminal = True
    auto = Automaton(vertices[0], set(vertices.values()))
    cur = -1
    for line in lines:
        if line[:1] == 'F':
            continue
        pos = line.find(':')
        if pos >= 0:
            cur = int(line[:pos])
        else:
            pos = line.find('>')
            sym = line[:pos]
            tos = list(map(int, line[pos + 2:].split()))
            vertices[cur].delta[sym] = set()
            for to in tos:
                vertices[cur].delta[sym].add(vertices[to])
    return auto


def nfa_to_str(auto: Automaton) -> str:
    sign(auto)
    by_index = [None] * len(auto.vertices)
    for vert in auto.vertices:
        by_index[vert.index] = vert
    output = ''
    for i in range(len(auto.vertices)):
        output += f"{i}:\n"
        vert = by_index[i]
        for sym, tos in vert.delta.items():
            output += f"{sym}>"
            for to in tos:
                output += f" {to.index}"
            output += '\n'
    output += 'F:'
    for vert in auto.vertices:
        if vert.terminal:
            output += f" {vert.index}"
    output += '\n'
    return output


def str_to_dfa(text: str) -> Automaton:
    lines = text.split('\n')
    sigma = lines[0].split()
    vertices = {}
    for i in range(1, len(lines) - 1):
        pos = lines[i].find(':')
        index = int(lines[i][:pos])
        vertices[index] = Vertex(False, {}, index)
    auto = Automaton(vertices[0], set(vertices.values()))
    for i in range(1, len(lines) - 1):
        pos = lines[i].find(':')
        index = int(lines[i][:pos])
        indexes = list(map(int, lines[i][pos + 2:].split()))
        for j in range(len(sigma)):
            if indexes[j] >= 0:  # -1 if no transition
                vertices[index].delta[sigma[j]] = {vertices[indexes[j]]}
    fins = list(map(int, lines[-1][3:].split()))
    for fin in fins:
        vertices[fin].terminal = True
    return auto


def dfa_to_str(auto: Automaton) -> str:
    syms = set()
    for vert in auto.vertices:
        syms |= set(vert.delta.keys())
    sigma = list(syms)
    output = ''
    output += ' '.join(map(str, sigma))
    output += '\n'
    sign(auto)
    by_index = [None] * len(auto.vertices)
    for vert in auto.vertices:
        by_index[vert.index] = vert
    for i in range(len(auto.vertices)):
        vert = by_index[i]
        output += f"{i}:"
        for sym in sigma:
            if sym in vert.delta.keys():
                output += f" {next(iter(vert.delta[sym])).index}"
            else:
                output += " -1"
        output += '\n'
    output += 'F:'
    for vert in auto.vertices:
        if vert.terminal:
            output += f" {vert.index}"
    output += '\n'
    return output
