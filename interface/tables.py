from tabulate import tabulate
from typing import List
from pathlib import Path


def print_determinization(table, sigma) -> (List[str], List[List[str]]):
    my_headers = [''] + sigma
    my_formatted_table = [[",".join(map(str, [vert.index for vert in row])) for row in rows] for rows in table]
    print(tabulate(my_formatted_table, headers=my_headers, tablefmt="grid"))
    return my_headers, my_formatted_table


def print_minimization(tables, sigma) -> (List[str], List[List[List[str]]]):
    my_headers = ['index', 'class'] + sigma
    output = []
    for i in range(len(tables)):
        table = tables[i]
        print(f"Step {i+1}/{len(tables)}:")
        my_formatted_table = [[str(j)] + [str(i) for i in line] for j, line in enumerate(table)]
        output.append(my_formatted_table)
        print(tabulate(my_formatted_table, headers=my_headers, tablefmt="grid"))
        print()
    return my_headers, output


def table_to_latex(my_headers: List[str], my_formatted_table: List[List[str]]) -> str:
    latex_table = "\\begin{tabular}{" + "|c" * len(my_headers) + "|}\n"
    latex_table += "\\hline\n"

    latex_table += " & ".join(my_headers) + " \\\\\n"
    latex_table += "\\hline\n"

    for row in my_formatted_table:
        latex_table += " & ".join(row) + " \\\\\n"
        latex_table += "\\hline\n"

    latex_table += "\\end{tabular}"

    return latex_table


def tables_to_latex(my_headers: List[str], my_formatted_tables: List[List[List[str]]]) -> List[str]:
    output = []
    for my_formatted_table in my_formatted_tables:
        output.append(table_to_latex(my_headers, my_formatted_table))
    return output


folder = Path('output/latex')


def save_table(filename: str, my_headers: List[str], my_formatted_table: List[List[str]]) -> None:
    with open(folder / filename, 'w') as file:
        file.write(table_to_latex(my_headers, my_formatted_table))


def save_tables(filename: str, my_headers: List[str], my_formatted_tables: List[List[List[str]]]) -> None:
    with open(folder / filename, 'w') as file:
        tables = tables_to_latex(my_headers, my_formatted_tables)
        for i, table in enumerate(tables):
            file.write(f"Step {i + 1}/{len(tables)}:\n\n")
            file.write(table)
            file.write('\n\n')
