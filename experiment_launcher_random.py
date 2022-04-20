import os
from pathlib import Path
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Run the tests for the random measurements approach')
parser.add_argument('--dryrun', action='store_true')
args = parser.parse_args()
dry_run = args.dryrun
n_to_time = {24:"3:59", 48:"3:59", 96:"3:59", 192:"23:59", 384:"23:59", 768:"123:59"}
n_to_mem = {24:"1000", 48:"4000", 96:"4000", 192:"10000", 384:"10000", 768:"10000"}
for n in [16, 32, 64, 128, 256]:
    n = 3*n//2 
    for degree in [2, 3, 4, 5]:
        my_range = np.linspace(0.1 * degree*np.log2(n), 2.5 * degree*np.log2(n), 40)
        m_list = [int(a) for a in my_range]
        for m in m_list:
            for try_no in range(10):
            # print(f"bsub -W 3:59 -o logs/log_n={n}_m={m}_d={degree}_{try_no}.out -R rusage[mem=10000] python -u scip_solver.py {n} {m} {degree} {try_no}")
                path = Path(f"results/n={n}_m={m}_d={degree}_{try_no}.json")
                if path.is_file():
                    submit_string = f"bsub -W {n_to_time[n]} -o logs/log_n={n}_m={m}_d={degree}_{try_no}.out -R rusage[mem={n_to_mem[n]}] python -u scip_solver.py {n} {m} {degree} {try_no}  &> /dev/null"
                    if not dry_run:
                        os.system(submit_string)
                    print(submit_string)
