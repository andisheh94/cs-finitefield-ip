import os
from pathlib import Path
import numpy as np
from math import ceil
import argparse
parser = argparse.ArgumentParser(description='Run the tests for the random binning approach')
parser.add_argument('--dryrun', action='store_true')
parser.add_argument('size', type=str)
args = parser.parse_args()
dry_run, size = args.dryrun, args.size
if size == "big":
    n_list = [1024, 2048, 4096, 8192]
elif size == "small":
    n_list = [16, 32, 64, 128, 256, 512]
else:
    n_list = []
for n in n_list:
    n = 3*n //2
    for degree in [2, 3, 4, 5, 6, 7, 8, 10, 20]:
        no_bins_range = np.linspace(0.2 * degree ** 2 if degree < 10 else 0.05 * degree ** 2,
                                    degree ** 2 if degree < 10 else 0.5 * degree ** 2, 10)
        no_bins_range = [ceil(a) for a in no_bins_range]
        for no_bins in no_bins_range:
            for no_iterations in [1, 2, 3]:
                for ratio in [1.1, 1.3, 1.5, 1.9, 2.1, 3.0]:
                    submit_string = ""
                    for try_no in range(10):
                        path = Path(
                            f"results2/n={n}_nobins={no_bins}_no_iter={no_iterations}_ratio={ratio}_d={degree}_{try_no}.json")
                        # if True:
                        if not path.is_file():
                            submit_string = submit_string + f"python -u random_binning.py {n} {no_bins} {no_iterations} {ratio} {degree} {try_no}"
                            if try_no != 9:
                                submit_string = submit_string + " && "
                    if submit_string != "":
                        submit_string = "bsub -W 0:20" \
                                        f" -o logs2/log_n={n}_nobins={no_bins}_no_iter={no_iterations}_ratio={ratio}_d={degree}.txt" \
                                        f" -R rusage[mem=10000] \"{submit_string}\" " \
                                        f"&> /dev/null"
                        if not dry_run:
                            os.system(submit_string)
                        print(submit_string)