# from graphviz import Digraph
from models.auto import Automaton
from operations.transform import sign
from pathlib import Path


warning = """# To use the graph visualisation you have to install the program (not only the lib) graphviz from https://graphviz.org/download/ .
# You should also add it to your system's PATH variable.
# If you have already done it switch on the installed flag (the boolean variable in graph.py modeule)."""
installed = False

folder = Path('output/graph')

if installed:
    graphviz = __import__('graphviz')
    Digraph = graphviz.Digraph


def visualize_automaton(auto: Automaton, name: str = 'automaton', to_sign: bool = False) -> None:
    if not installed:
        print(warning)
        print()
        return

    dot = Digraph()

    if to_sign:
        sign(auto)

    for vert in auto.vertices:
        shape = 'doublecircle' if vert.terminal else 'circle'
        dot.node(f'q{vert.index}', shape=shape, label=f'q{vert.index}')

    dot.node('start', shape='none', label='')
    dot.edge('start', 'q0')

    for vert in auto.vertices:
        for symbol, states in vert.delta.items():
            for j, state in enumerate(states):
                label = symbol if symbol != '' else 'ε'
                dot.edge(f'q{vert.index}', f'q{state.index}', label=label)

    dot.render(folder / name, view=True, format='png')


