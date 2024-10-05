import json
from typing import Dict
from models.auto import Automaton, Vertex
from pathlib import Path
from operations.transform import sign


output_folder = Path('output')
input_folder = Path('input')


def save_automaton(auto: Automaton, filename: str) -> None:
    sign(auto)

    data = {
        "s0": f"s{auto.start.index}",
        "states": [str(vert.index) for vert in auto.vertices],
        "final": [str(vert.index) for vert in auto.vertices if vert.terminal],
        "delta": []
    }

    for v in auto.vertices:
        for symbol, targets in v.delta.items():
            for target in targets:
                data["delta"].append({
                    "from": f"s{v.index}",
                    "to": f"s{target.index}",
                    "sym": symbol
                })

    with open(output_folder / filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_automaton(filename: str) -> Automaton:
    with open(input_folder / filename, 'r') as f:
        data = json.load(f)

    indexes = {data["s0"]: 0}
    counter = 1
    for state in data["states"]:
        if state != data["s0"]:
            indexes[state] = counter
            counter += 1

    terminals = {key: False for key in indexes}
    for state in data["final"]:
        terminals[state] = True

    # create all vertices (initially without transitions)
    vertices: Dict[str, Vertex] = {}
    for state in data["states"]:
        vertices[state] = Vertex(
            terminal=terminals[state],
            delta={},
            index=indexes[state]
        )

    # add transitions (delta)
    for transition in data["delta"]:
        from_vertex = vertices[transition["from"]]
        to_vertex = vertices[transition["to"]]
        symbol = transition["sym"]

        if symbol not in from_vertex.delta:
            from_vertex.delta[symbol] = set()
        from_vertex.delta[symbol].add(to_vertex)

    start_vertex = vertices[data["s0"]]

    return Automaton(start=start_vertex, vertices=set(vertices.values()))
