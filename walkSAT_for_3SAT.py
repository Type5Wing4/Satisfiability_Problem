import sys
import re
import numpy
import random

class simple_walkSAT_001():

    def __init__(self, output_each_step=True):

        self.output_each_step = output_each_step


    def read_cnf_format_problem_file(self, cnf_file_name):

        f = open(cnf_file_name, 'r')
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

        self.clauses = clauses
        self.nb_vars = nb_vars

    def set_initial_values(self):

        xs = []
        for i in range(self.nb_vars):
            if random.random() > 0.50:
                xs.append(0)
            else:
                xs.append(1)

        return xs

    def judge_sat_and_unsat_clauses(self, xs):

        # Calc F with current xs.
        # If there is no unsatisfied clause, F is True, i.e. Satisfied. 
        sat_clause_indices = []
        unsat_clause_indices = []
        clause_num = 0
        for clause in self.clauses:

            ith_clause = False
            for x in clause:
                if x > 0 and xs[x-1] == 1:
                    ith_clause = ith_clause or True
                elif x < 0 and xs[abs(x)-1] == 0:
                    ith_clause = ith_clause or True 
                else:
                    pass

            if ith_clause:
                sat_clause_indices.append(clause_num)
            else:
                unsat_clause_indices.append(clause_num)
            clause_num += 1

        return sat_clause_indices, unsat_clause_indices

    def select_x_to_be_flipped(self, xs, sat_clause_indices, unsat_clause_indices, p=0.2):

        '''
        WalkSAT first picks a clause which is unsatisfied by the current assignment,
        then flips a variable within that clause.
        The clause is picked at random among unsatisfied clauses.
        The variable is picked that will result in the fewest previously satisfied clauses
        becoming unsatisfied, with some probability of picking one of the variables at random.

        '''

        selected_clause_index = random.choice(unsat_clause_indices)
        if random.random() > p:
            nb_clauses_from_sat_to_unsat_list = []
            for t in self.clauses[selected_clause_index]:

                nb_clauses_from_sat_to_unsat = 0

                for j in sat_clause_indices:

                    if t in self.clauses[j] or -t in self.clauses[j]:

                        ith_clause = False
                        for x in self.clauses[j]:

                            if abs(t) == abs(x):
                                if x > 0 and 1 - xs[x-1] == 1:
                                    ith_clause = ith_clause or True
                                elif x < 0 and 1 - xs[abs(x)-1] == 0:
                                    ith_clause = ith_clause or True 
                                else:
                                    pass
                            else:
                                if x > 0 and xs[x-1] == 1:
                                    ith_clause = ith_clause or True
                                elif x < 0 and xs[abs(x)-1] == 0:
                                    ith_clause = ith_clause or True 
                                else:
                                    pass

                            if not ith_clause:
                                nb_clauses_from_sat_to_unsat += 1 
                nb_clauses_from_sat_to_unsat_list.append(nb_clauses_from_sat_to_unsat)

            min_val = len(self.clauses)
            num = 0
            for nb_clauses_break in nb_clauses_from_sat_to_unsat_list:
                if min_val > nb_clauses_break:
                    min_val = nb_clauses_break
                    candidate_vars = [abs(self.clauses[selected_clause_index][num])]
                elif min_val == nb_clauses_break:
                    candidate_vars.append(abs(self.clauses[selected_clause_index][num]))
                num += 1

            x_to_be_flipped = random.choice(candidate_vars)

        else:
            x_to_be_flipped = abs(random.choice(self.clauses[selected_clause_index]))

        return x_to_be_flipped

    def main(self, cnf_file_name, nb_max_steps, p):

        self.read_cnf_format_problem_file(cnf_file_name)
        xs = self.set_initial_values()

        solved = False
        for steps in range(nb_max_steps):

            sat_clause_indices, unsat_clause_indices = self.judge_sat_and_unsat_clauses(xs)

            if unsat_clause_indices == []:
                solved = True
                break

            x_to_be_flipped = self.select_x_to_be_flipped(xs, sat_clause_indices, unsat_clause_indices, p)

            xs[x_to_be_flipped-1] = 1 - xs[x_to_be_flipped-1]

            if self.output_each_step:
                print(steps+1, xs)

        # Output results
        if solved:
            print()
            print('Successfully founded a solution at ', steps, ' steps.')
            print(xs)
        else:
            print('Not found within ', nb_max_steps, ' steps.')
        

if __name__ == '__main__':

    cnf_file_name = sys.argv[1]
    swsat = simple_walkSAT_001(output_each_step=False)
    swsat.main(cnf_file_name, nb_max_steps=50000, p=0.2)

