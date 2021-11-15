import os
import numpy as np
for n in [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
    for degree in [2, 3, 5, 10]:
        my_range = np.arange(degree*np.log2(n), 4 * degree*np.log2(n), 10)
        m_list = [int(a) for a in my_range]
        for m in m_list:
            for try_no in range(20):
                #print(f"python scip_solver.py {n} {m} {degree} {try_no}")
                os.system(f"python scip_solver.py {n} {m} {degree} {try_no}")
