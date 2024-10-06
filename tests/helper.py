def compare_states(state1, state2) -> bool:
    state1.sort()
    state2.sort()
    return state1 == state2


def compare_finals(final1, final2) -> bool:
    final1.sort()
    final2.sort()
    return final1 == final2


def compare_deltas(delta1, delta2) -> bool:
    for trans1 in delta1:
        flag = False
        for trans2 in delta2:
            if trans1 == trans2:
                flag = True
                break
        if not flag:
            return False
    for trans2 in delta2:
        flag = False
        for trans1 in delta1:
            if trans1 == trans2:
                flag = True
                break
        if not flag:
            return False
    return True
