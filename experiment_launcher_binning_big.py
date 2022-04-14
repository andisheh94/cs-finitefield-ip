import os
from pathlib import Path
import numpy as np
from math import ceil
submitted_jobs = set()
for n in [1024, 2048, 4096, 8192]:
    n = 3*n //2
    for degree in [2, 4, 6, 8, 10, 20]:
        no_bins_range = np.linspace(0.2 * degree**2,  degree**2, 10)
        no_bins_range = [ceil(a) for a in no_bins_range]
        for no_bins in no_bins_range:
            for no_iterations in [1, 2, 3]:
                for ratio in [1.1, 1.3, 1.5, 1.9, 2.1, 3.0]:
                    for try_no in range(10):
                        path = Path(f"results2/n={n}_nobins={no_bins}_no_iter={no_iterations}_ratio={ratio}_d={degree}_{try_no}.json")
                        # if True:
                        if not path.is_file():
                            submit_string = f"bsub -W 0:20"\
                                            f" -o logs2/log_n={n}_nobins={no_bins}_no_iter={no_iterations}_ratio={ratio}_d={degree}_{try_no}.json"\
                                            f" -R rusage[mem=1000] "\
                                            f"python -u random_binning.py {n} {no_bins} {no_iterations} {ratio} {degree} {try_no} "\
                                            f"&> /dev/null"

                            if submit_string not in submitted_jobs:
                                # os.system(submit_string)
                                print(submit_string)
                                submitted_jobs.add(submit_string)
