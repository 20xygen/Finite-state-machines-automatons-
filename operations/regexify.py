from models.auto import Automaton, Vertex
from typing import Dict, Set, Optional, List
from models.bidirectional import BidirectionalVertex, BidirectionalAutomaton


def multiplier(rx: str):
    if len(rx) <= 1 or rx.count('+') == 0:
        return rx
    else:
        return f"({rx})"


def base(rx: str):
    if len(rx) <= 1:
        return rx
    else:
        return f"({rx})"


def rx_from_syms(syms: List[str], star: bool = False) -> str:
    syms = [sym if sym != '' else '_' for sym in syms]
    if len(syms) == 0:
        rx = ''
    elif len(syms) == 1:
        if star:
            rx = base(syms[0]) + '*'
        else:
            rx = syms[0]
    else:
        rx = '+'.join(syms)
        if star:
            rx = base(rx) + '*'
    return rx


def to_regex(auto: Automaton) -> str:  # given automaton will NOT be affected
    bi = BidirectionalAutomaton(auto, single_end=True)

    by_index = [None] * len(bi.vertices)  # index -> vertex
    for vert in bi.vertices:
        by_index[vert.index] = vert

    for i in range(1, len(by_index) - 1):
        vert: BidirectionalVertex = by_index[i]
        self_syms = [sym for sym, tos in vert.delta.items() if vert in tos]  # loops
        self_rx = rx_from_syms(self_syms, True)
        for prefix, left_set in vert.reverse.items():  # process all transitions vertex -> vert -> vertex
            for left in left_set:
                if left != vert:
                    for suffix, right_set in vert.delta.items():
                        for right in right_set:
                            if right != vert:
                                rx = ''
                                rx += multiplier(prefix)
                                rx += self_rx
                                rx += multiplier(suffix)
                                if rx not in left.delta.keys():
                                    left.delta[rx] = set()
                                if rx not in right.reverse.keys():
                                    right.reverse[rx] = set()
                                left.delta[rx].add(right)
                                right.reverse[rx].add(left)

        # cur copied edges
        for prefix, left_set in vert.reverse.items():
            for left in left_set:
                if left != vert:
                    left.delta[prefix].remove(vert)
        for suffix, right_set in vert.delta.items():
            for right in right_set:
                if right != vert:
                    right.reverse[suffix].remove(vert)
        vert.delta = {}
        vert.reverse = {}

    # now automaton is ->(q0 with loops)->(ending conditions)
    left_syms = [sym for sym, vert_set in bi.start.reverse.items() if len(vert_set) > 0]
    left_rx = rx_from_syms(left_syms, True)
    mid_syms = [sym for sym, vert_set in bi.end.reverse.items() if len(vert_set) > 0]
    mid_rx = rx_from_syms(mid_syms)
    return multiplier(left_rx) + multiplier(mid_rx)

