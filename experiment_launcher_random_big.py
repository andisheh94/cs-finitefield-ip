import os
from pathlib import Path
import numpy as np
for n in [512, 1024, 2048]:
    n = 3*n //2 
    for degree in [2, 3, 4, 5, 6]:
        my_range = np.linspace(0.4 *degree*np.log2(n), 6 * degree*np.log2(n), 50)
        m_list = [int(a) for a in my_range]
        for m in m_list:
            for try_no in range(20):
                path = Path(f"results/n={n}_m={m}_d={degree}_{try_no}.json")
                # if True:
                if not path.is_file():
                    os.system(f"bsub -W 23:59 -o logs/log_n={n}_m={m}_d={degree}_{try_no}.out -R rusage[mem=20000] python -u scip_solver.py {n} {m} {degree} {try_no} &> /dev/null")
                    print(f"bsub -W 23:59 -o logs/log_n={n}_m={m}_d={degree}_{try_no}.out -R rusage[mem=20000] python -u scip_solver.py {n} {m} {degree} {try_no} &> /dev/null")
