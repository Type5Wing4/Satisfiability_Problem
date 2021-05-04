import sys
import re
import numpy
import random

def simple_walkSAT_for_3SAT(benchmark_problem, nb_max_steps, p=0.2):

    # Read benchmark problem file (cnf format).
    f = open(benchmark_problem, 'r')
    lines = f.readlines()

    clauses = []
    for line in lines:
        if line[0] == 'c': 
            continue
        elif line[0] == 'p':
            for xi in re.split(' [ ]*', line):
                nb_vars_index = 1 + re.split(' [ ]*', line).index('cnf')
                nb_vars = int(re.split(' [ ]*', line)[nb_vars_index])
        elif line[0] == '%':
            break
        else:
            clauses_i = []
            for xi in re.split(' [ ]*', line):
                if xi != '':
                    clauses_i.append(int(xi)) 
                    if len(clauses_i) == 3:
                        break
            clauses.append(clauses_i)

    # Set initial values.
    xs = []
    for i in range(nb_vars):
        if random.random() > 0.50:
            xs.append(0)
        else:
            xs.append(1)

    print(0, xs)

    solved = False
    for steps in range(nb_max_steps):

        sat_clause_indices = []
        unsat_clause_indices = []
        clause_num = 0
        for clause in clauses:

            ith_clause = False
            for x in clause:
                if x > 0 and xs[x-1] == 1:
                    ith_clause = ith_clause or True
                elif x < 0 and xs[abs(x)-1] == 0:
                    ith_clause = ith_clause or True 
                else:
                    ith_clause = ith_clause or False

            if ith_clause:
                sat_clause_indices.append(clause_num)
            else:
                unsat_clause_indices.append(clause_num)
            clause_num += 1

        if unsat_clause_indices == []:
            solved = True
            break

        selected_clause_index = random.choice(unsat_clause_indices)
        if random.random() > p:
            break_cause_indices = []
            nb_clauses_to_unsat_from_sat_list = []
            for t in clauses[selected_clause_index]:

                nb_clauses_to_unsat_from_sat = 0

                for j in sat_clause_indices:

                    if t in clauses[j] or -t in clauses[j]:

                        ith_clause = False
                        for x in clauses[j]:
                            if abs(t) == abs(x):
                                if x > 0 and 1 - xs[x-1] == 1:
                                    ith_clause = ith_clause or True
                                elif x < 0 and 1 - xs[abs(x)-1] == 0:
                                    ith_clause = ith_clause or True 
                                else:
                                    ith_clause = ith_clause or False
                            else:
                                if x > 0 and xs[x-1] == 1:
                                    ith_clause = ith_clause or True
                                elif x < 0 and xs[abs(x)-1] == 0:
                                    ith_clause = ith_clause or True 
                                else:
                                    ith_clause = ith_clause or False

                            if not ith_clause:
                                nb_clauses_to_unsat_from_sat += 1 
                nb_clauses_to_unsat_from_sat_list.append(nb_clauses_to_unsat_from_sat)

            min_val = len(clauses)
            num = 0
            for nb_clauses_break in nb_clauses_to_unsat_from_sat_list:
                if min_val > nb_clauses_break:
                    min_val = nb_clauses_break
                    candidate_vars = [abs(clauses[selected_clause_index][num])]
                elif min_val == nb_clauses_break:
                    candidate_vars.append(abs(clauses[selected_clause_index][num]))
                num += 1

            x_to_be_flipped = random.choice(candidate_vars)

        else:
            x_to_be_flipped = abs(random.choice(clauses[selected_clause_index]))

        xs[x_to_be_flipped-1] = 1 - xs[x_to_be_flipped-1]
        print(steps+1, xs)

    if solved:
        print()
        print('Successfully founded a solution.')
        print(xs)
    else:
        print('Not found within ', nb_max_steps, ' steps.')


if __name__ == '__main__':

    benchmark_problem = sys.argv[1]
    simple_walkSAT_for_3SAT(benchmark_problem, nb_max_steps=50000)
