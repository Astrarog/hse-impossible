from kb_anlysis.shrinking.operators import *
from kb_anlysis.useful_functions import *


def continue_condition(x):
    return x != get_bits(255)


inp_diff = set()
out_diff = set()
imp_diff = set()
print("Input differentials of probability 1 for 3 or more rounds:")
for n in range(1, 255):
    x = get_bits(n)
    rounds, diff = max_transformation(x, kb_forward, continue_condition)
    diff = tuple(diff)
    x = tuple(x)
    if rounds >= 3:
        inp_diff.add((x, diff, rounds))
        print(f"{x} -> {diff} with {rounds} rounds")

print()
print("Output differentials of probability 1 for 3 or more rounds:")
for n in range(1, 255):
    y = get_bits(n)
    rounds, diff = max_transformation(y, kb_backward, continue_condition)
    diff = tuple(diff)
    y = tuple(y)
    if rounds >= 3:
        out_diff.add((y, diff, rounds))
        print(f"{y} -> {diff} with {rounds} rounds")

f = open("results_shrinking.csv", 'w')

header_list = ['deltax', 'nx', 'deltay', 'ny', 'n']
header = ";".join(header_list) + '\n'
f.write(header)

for (x, diff_x, nx) in inp_diff:
    for (y, diff_y, ny) in out_diff:
        if diff_y != diff_x:
            print(f"IMPOSSIBLE {nx+ny} {x} -> {diff_x} != {diff_y} <- {y}")
            idiff = (x, nx, y, ny, nx+ny)
            imp_diff.add(idiff)

            data = list(map(str, (x, nx, y, ny, nx+ny)))
            string = (";".join(data) + '\n').replace('1', r'\circ')
            f.write(string)

print(f"Found {len(imp_diff)} impossible differentials with length of 6 rounds or more")
f.close()
