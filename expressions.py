from kb_anlysis.expressions.XorExpression import XorExpression
from kb_anlysis.expressions.KB256 import KB256
from kb_anlysis.expressions.LatexCreator import LatexCreator
from itertools import permutations
from collections import Counter


alphabet = 'abcdefgh'

def has_single_difference(x):
    occurences = Counter(x)
    occurences.pop(0, None)
    occurences = list(occurences.values())
    occurences.sort()
    occurences = tuple(occurences)
    return len(occurences) <= 1

def is_same_for_modulus(x, y):    
    return has_single_difference(x) and has_single_difference(y)

def check_differential(x, y):
    found_almost_impossible = False
    for i in range(len(x)):
        
        equation = set(XorExpression([x[i], y[i]]))

        immutable = set(['f1', 'f2', 'f3']) | set(['g1', 'g2', 'g3']) | set('abcdefgh')
        
        if len(set(equation)) == 1 and set() != (immutable & equation):
            return 'impossible'
        
        found_almost_impossible = found_almost_impossible or (equation != XorExpression())
    
    if found_almost_impossible:
        return 'almost_impossible'
    
    return 'possible'

def continue_condition_for_impossible(x):
    cont = True
    for e in x:
        for check in {'f1', 'f2', 'f3', 'g1', 'g2', 'g3'}:
            if (check in str(e)):
                return False
    return True

def get_max_depth(x, kb_transform):
    i = 1
    prev = x
    y = kb_transform(x, i)
    while XorExpression() in y:
        i += 1
        prev = y
        y = kb_transform(x, i)
        
    return i-1, prev

def get_impossible_depth(x, kb_transform):
    i = 1
    y = kb_transform(x, i)
    while continue_condition_for_impossible(y):
        i += 1
        y = kb_transform(x, i)
    return i-1, y

def gen_letter():
    for l in alphabet:
        yield l

def get_experiment_seeds():
    experiment_seeds = [ [0] * 8 ]
    experiments_for_current_letter = experiment_seeds.copy()
    current_alphabet = set()
    letter_generator = gen_letter()
    for i in range(1, 9):
        add_zeros = lambda x: list(x) + [0 for _ in range(8 - i)]
        current_alphabet.add(next(letter_generator))
        
        prev_experiments = experiments_for_current_letter[:]
        experiments_for_current_letter = list()
        experiments_candidates = list()
        for e in prev_experiments:
            for letter in current_alphabet:
                experiments_candidates += [[letter] + e[:-1]]
    
        known_valid_experiments = set()        
        for permutation in experiments_candidates:
            occurences = Counter(permutation)
            occurences.pop(0, None)
            occurences = list(occurences.values())
            occurences.sort()
            occurences = tuple(occurences)
            if occurences not in known_valid_experiments:
                known_valid_experiments.add(occurences)
                experiment_seeds += [ permutation ]
                experiments_for_current_letter += [ permutation ]
                
    return experiment_seeds


def get_tranformations():
    experiment_seeds = get_experiment_seeds()[1:]
    
    kb = KB256()
    
    print("Encrypt differentials:")
    enc_diffs_max_depth = dict()
    dec_diffs_max_depth = dict()
    
    enc_impossible = dict()
    dec_impossible = dict()
    count_done = 0
    for seed in experiment_seeds:
        print()
        experiments = set(permutations(seed))
        print(f"Starting {len(experiments)} experiments")
        for e in experiments:
            enc_max_depth_rounds, enc_max_depth_diff = get_max_depth(e, kb.encrypt_n)
            dec_max_depth_rounds, dec_max_depth_diff = get_max_depth(e, kb.decrypt_n)
    
            enc_impossible_rounds, enc_impossible_diff = get_impossible_depth(e, kb.encrypt_n)
            dec_impossible_rounds, dec_impossible_diff = get_impossible_depth(e, kb.decrypt_n)
    
            if (enc_max_depth_rounds >= 4):
                enc_diffs_max_depth[tuple(e)] = (enc_max_depth_rounds, enc_max_depth_diff)
                print(f"enc {e} -> {enc_max_depth_diff} with {enc_max_depth_rounds} rounds for max depth")
    
            if (dec_max_depth_rounds >= 4):
                dec_diffs_max_depth[tuple(e)] = (dec_max_depth_rounds, dec_max_depth_diff)
                print(f"dec {e} -> {dec_max_depth_diff} with {dec_max_depth_rounds} rounds for max depth")
    
        
            if (enc_impossible_rounds >= 4):
                enc_impossible[tuple(e)] = (enc_impossible_rounds, enc_impossible_diff)
                print(f"enc {e} -> {enc_impossible_diff} with {enc_impossible_rounds} rounds for impossible")
    
            if (dec_impossible_rounds >= 4):
                dec_impossible[tuple(e)] = (dec_impossible_rounds, dec_impossible_diff)
                print(f"dec {e} -> {dec_impossible_diff} with {dec_impossible_rounds} rounds for impossible")
    
        count_done += 1
        print(f"Done {count_done}/{len(experiment_seeds)} seeds")
    
    print()
    print()
    print()
    print(f"In total saved {len(enc_diffs_max_depth)} transformations for max depth encryption")
    print(f"In total saved {len(dec_diffs_max_depth)} transformations for max depth decryption")
    print(f"In total saved {len(enc_impossible)} transformations for impossible encryption")
    print(f"In total saved {len(dec_impossible)} transformations for impossible decryption")
    print()
    print()
    print()
    
    return enc_diffs_max_depth, dec_diffs_max_depth, enc_impossible, dec_impossible

def find_trancformations_possibility(enc_transforms, dec_transforms):
    impossible = set()
    almost_impossible = set()

    print()
    print(f"Cheking for {len(enc_transforms) * len(dec_transforms)} differentials")
    for x_start in enc_transforms:
        (n, x_middle) = enc_transforms[x_start]
        for y_finish in dec_transforms:
            (m, y_middle) = dec_transforms[y_finish]
            status = check_differential(x_middle, y_middle)
            
            diff = (tuple(x_start), n, tuple(y_finish), m, status) 
            if status == 'impossible':
                print(f"IMPOSSIBLE {n+m} {x_start} -> {x_middle} != {y_middle} <- {y_finish}")
                impossible.add(diff)
            if status == 'almost_impossible':
                print(f"ALMOST {n+m} {x_start} -> {x_middle} != {y_middle} <- {y_finish}")
                almost_impossible.add(diff)
    
    print(f"Found {len(impossible)} impossible differentials")
    print(f"Found {len(almost_impossible)} almost impossible differentials")
    return impossible, almost_impossible
    
impossible = set()
almost_impossible = set()
enc_diffs_max_depth, dec_diffs_max_depth, enc_impossible, dec_impossible = get_tranformations()

i, a = find_trancformations_possibility(enc_impossible, dec_impossible)
impossible |= i
almost_impossible |= a

i, a = find_trancformations_possibility(enc_impossible, dec_diffs_max_depth)
impossible |= i
almost_impossible |= a

i, a = find_trancformations_possibility(enc_diffs_max_depth, dec_impossible)
impossible |= i
almost_impossible |= a

i, a = find_trancformations_possibility(enc_diffs_max_depth, dec_diffs_max_depth)
impossible |= i
almost_impossible |= a

impossible_and_almost = impossible | almost_impossible

print()
print(f"IN TOTAL Found {len(impossible)} impossible differentials")
print(f"IN TOTAL Found {len(almost_impossible)} almost impossible differentials")
print()

header_list = ['deltax', 'nx', 'deltay', 'ny', 'n', 'status']

single_header = ";".join(header_list[:-1]) + '\n'
combined_header = ";".join(header_list) + '\n'

f_impossible = open('results_impossible.csv', 'w')
f_almost = open('results_almost.csv', 'w')
f_modulus = open('results_modulus.csv', 'w')


f_impossible.write(single_header)
f_almost.write(single_header)
f_modulus.write(combined_header)

impossible_and_almost = list(impossible_and_almost)
impossible_and_almost.sort(key=lambda x:x[1] + x[3], reverse=True)
cnt_i = 0
cnt_a = 0
cnt_mi = 0
cnt_ma = 0

for e in impossible_and_almost:
    x, nx, y, ny, status = e
    s = ''
    
    f_single = None
    if status == 'impossible':
        s = 'I'
        f_single = f_impossible

    else:
        s = 'A'
        f_single = f_almost
    
    
    
    if is_same_for_modulus(x, y):
        if s == 'I':
            cnt_mi += 1
        else:
            cnt_ma += 1 
        data_modulus = list(map(str, (x, nx, y, ny, nx+ny, s)))
        string_modulus = (";".join(data_modulus) + '\n').replace("'", '').replace('a', '2^{31}')
        f_modulus.write(string_modulus)
    
    if e[1] + e[3] >= 14:
        if s == 'I':
            cnt_i += 1
        else:
            cnt_a += 1 
        data_single = list(map(str, (x, nx, y, ny, nx+ny)))
        string_single = (";".join(data_single) + '\n').replace("'", '')
        f_single.write(string_single)
    

        
print(f"Found {cnt_i} impossible differentials with length of 14 rounds or more")
print(f"Found {cnt_a} almost impossible differentials with length of 14 rounds or more")
print(f"Found {cnt_mi} impossible differentials for modulus addition with length of 8 rounds or more")
print(f"Found {cnt_ma} almost impossible differentials for modulus addition with length of 8 rounds or more")


f_impossible.close()
f_almost.close()
f_modulus.close()
