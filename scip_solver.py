import sys
import numpy as np
from pyscipopt import Model, quicksum
import time
import json
if __name__ == "__main__":
    n, m, degree, try_number  = [int(sys.argv[j]) for j in [1, 2, 3, 4]]
    np.random.seed(try_number)
    frequency = np.array([0] * n, dtype= int)
    # Frequency might not actually be degree exactly d since we are doing sampling with replacement
    support = np.array([np.random.randint(0, n) for _ in range(degree)], dtype=int)
    frequency[support] = 1
    cs_matrix = np.random.randint(0, 2, (m, n))
    y = np.dot(cs_matrix, frequency) % 2

    #Create a model instance
    start_time = time.time()
    model = Model()
    model.hideOutput()
    # Fix infeasibility bug
    model.setParam("presolving/maxrounds", 0)
    vars = [0] * n
    objective = None
    #Vars and objective
    for j in range(n):
        vars[j] = model.addVar(f'x_{j}', vtype="B")
        if j==0:
            objective = vars[0]
        else:
            objective = objective + vars[j]
    # add the constraints for measurments
    for i in range(m):
        cons = [vars[j] for j in range(n) if cs_matrix[i][j]==1]
        # print(cons)
        model.addConsXor(cons, True if y[i]==1 else False)
    # add extra constraint for degree
    model.addCons(quicksum(vars[j] for j in range(n)) <= degree )
    # Find solution
    model.optimize()
    sol = model.getBestSol()
    end_time = time.time()
    sol = np.array([int(sol[vars[j]]) for j in range(n)], dtype=int)
    # print(sol, frequency)
    result = {"status": np.array_equal(sol, frequency),  "time":end_time-start_time, \
              "n":n, "m":m, "d":degree
              }
    # print(result)
    with open(f"results/n={n}_m={m}_d={degree}_{try_number}.json", "w") as f:
        json.dump(result, f)
