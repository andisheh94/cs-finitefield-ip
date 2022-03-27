from pathlib import Path
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('--dryrun', action='store_false')
args = parser.parse_args()
for n in [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 9192, 2**14, 2**15, 2**16]:
    n = 3*n//2 
    for degree in [2 , 3, 4, 5]:
        path = Path(f"results3/n={n}_d={degree}.json")
        if not path.is_file():
            submit_string = f"bsub -W 123:59 "\
                            f" -o logs3/log_n={n}_d={degree}.txt"\
                            f" -R rusage[mem=40000] "\
                            f"python -u reed_solomon.py {n} {degree} "\
                            f"&> /dev/null"
            if args.dryrun:
                os.system(submit_string)
            print(submit_string)
