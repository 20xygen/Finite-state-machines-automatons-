from operations.poland import to_polish_notation, polska_into_auto
from operations.transform import determinate, minimize, make_complete, complement
from interface.graph import visualize_automaton
from interface.tables import print_determinization, print_minimization, tables_to_latex, table_to_latex, save_table, save_tables
from operations.regexify import to_regex
from interface.loader import save_automaton
from pathlib import Path
from interface.text import nfa_to_str, dfa_to_str, str_to_dfa, str_to_nfa
from facade.nfa import NFA
from facade.dfa import DFA


# FACADE EXAMPLES

with open(Path('input') / 'nfa.txt') as f:
    s = f.readlines()
    s = ''.join(s)

nfa1 = NFA(s)
# nfa1.visualize()
nfa1.save(Path('output') / 'nfa.txt')


with open(Path('input') / 'dfa.txt') as f:
    s = f.readlines()
    s = ''.join(s)

dfa1 = DFA(s)
# dfa1.visualize()
dfa1.save(Path('output') / 'dfa.txt')


nfa2 = NFA.by_regex("(ab+b)*a")
nfa2.print()
nfa2.visualize()
print(nfa2.regex())

print(nfa2.process("a"))  # True
print(nfa2.process("ababa"))  # True
print(nfa2.process("bbabba"))  # True
print(nfa2.process("aaba"))  # False
print(nfa2.process("ababab"))  # False
print(nfa2.process("c"))  # False


nfa3 = NFA.by_regex("aba+b(ab+bb)*b")
dfa2 = DFA.by_nfa(nfa3, True)  # True: the process of determinization will be printed
# dfa2.visualize()
dfa2.minimize(True)  # True: the process of minimization will be printed
dfa2.visualize()
print(dfa2.regex())
print(dfa2.process("bbbb"))
dfa2.complement()


# MANUAL EXAMPLES

sigma = ['a', 'b']

# By regex

regex = "(a(ab+b(ba)*a)*)*"
print("Regular expression:", regex)
polish_notation = to_polish_notation(regex)
print("Polish notation:", polish_notation)
auto = polska_into_auto(polish_notation)
visualize_automaton(auto, 'original', True)

# Determinization

table, det = determinate(auto, sigma)
visualize_automaton(det, 'determine', True)
my_det_h, my_det_f = print_determinization(table, sigma)
# save_automaton(det, 'first.json')
save_table('determinization.txt', my_det_h, my_det_f)

# Making complete

make_complete(det, sigma)
# visualize_automaton(det, 'full', True)
# save_automaton(det, 'second.json')

# Make complement

complement(det)
visualize_automaton(det, 'complement', True)
# save_automaton(mini, 'fifth.json')

# Minimization

tables, mini = minimize(det, sigma)
visualize_automaton(mini, 'minimized', True)
my_min_h, my_min_f = print_minimization(tables, sigma)
# save_automaton(mini, 'third.json')
save_tables('minimization.txt', my_min_h, my_min_f)
# save_automaton(mini, 'fourth.json')

# Regex by FA

rx = to_regex(mini)
print("Rugular expression:", rx)
