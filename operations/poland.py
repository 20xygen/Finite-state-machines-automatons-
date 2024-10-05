from models.auto import Automaton, Vertex
from operations.basic import merge, concatenate, star, plus
from typing import Optional


priority = {
    '^': 4,  # плюс Клини
    '*': 3,  # звезда Клини
    '.': 2,  # конкатенация
    '+': 1   # объединение
}


def is_operator(sym: str):
    return sym in {'*', '+', '.', '^'}


def is_symbol(sym: str):
    return sym.isalnum() or sym == '_'


def add_concatenation(regex):
    result = []
    for i in range(len(regex) - 1):
        result.append(regex[i])
        if (is_symbol(regex[i]) or regex[i] == ')' or regex[i] == '*' or regex[i] == '^') and \
                (is_symbol(regex[i + 1]) or regex[i + 1] == '('):
            result.append('.')
    result.append(regex[-1])
    return ''.join(result)


def to_polish_notation(regex):
    if len(regex) == 0:
        raise ValueError('Empty regex')
    regex = add_concatenation(regex)
    output = []
    operators = []

    for char in regex:
        if is_symbol(char):
            output.append(char)

        elif char == '(':
            operators.append(char)

        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()

        elif is_operator(char):
            while operators and operators[-1] != '(' and priority[operators[-1]] >= priority[char]:
                output.append(operators.pop())
            operators.append(char)

    while operators:
        output.append(operators.pop())

    return ''.join(output)


def char_into_auto(sym: str) -> Automaton:
    end = Vertex(True, {})
    start = Vertex(False, {sym: {end}})
    return Automaton(start, {start, end})


def polska_into_auto(polska: str) -> Optional[Automaton]:
    buffer = []
    last = -1
    for sym in polska:
        if sym == '.':
            buffer[last - 1] = concatenate(buffer[last - 1], buffer[last])
            buffer.pop(last)
            last -= 1
        elif sym == '+':
            buffer[last - 1] = merge(buffer[last - 1], buffer[last])
            buffer.pop(last)
            last -= 1
        elif sym == '*':
            buffer[last] = star(buffer[last])
        elif sym == '^':
            buffer[last] = plus(buffer[last])
        else:
            last += 1
            buffer.append(char_into_auto(sym if sym != '_' else ''))
    if last == 0:
        return buffer[0]
    else:
        return None