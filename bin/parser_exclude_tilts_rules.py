#!/fs/pool/pool-plitzko3/Michael/02-Software/python/conda3/envs/cryotherapy/bin/python

import argparse
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

from src.lib.exclude_tilts.exclude_tilts_rules import Main

def parse_arguments():
    parser = argparse.ArgumentParser(description="Rule based exclusion")
    parser.add_argument("--in_mics", "-in_mics", help="Input tilt series STAR file")
    parser.add_argument("--o", dest="out_dir", help="Output directory name")
    parser.add_argument("--s_min", "-shift_min", help="threshold min movement")
    parser.add_argument("--s_max", "-shift_max", help="threshold max movement")
    parser.add_argument("--d_min", "-defocus_min", help="threshold min defocus")
    parser.add_argument("--d_max", "-defocus_max", help="threshold max defocus")
    parser.add_argument("--r_min", "-resolution_min", help="threshold min resolution")
    parser.add_argument("--r_max", "-resolution_max", help="threshold max resolution")
    parser.add_argument("--j", "-nr_threads", help="Nr of threads used. Ignore!")
    return parser.parse_args()

def main():
    args = parse_arguments()

    python_script = os.path.join(root_dir, "src/lib/exclude_tilts/exclude_tilts_rules.py")
    python_command = f"python3 {python_script} --in_mics {args.in_mics} --o {args.out_dir} --s_min {args.s_min} --s_max {args.s_max} --d_min {args.d_min} --d_max {args.d_max} --r_min {args.r_min} --r_max {args.r_max} --j {args.j}"
    python_exit_status = os.system(python_command)

    # Redirect stdout and stderr to files
    os.chdir(args.out_dir)
    with open("run.out", "w") as out_file:
        sys.stdout = out_file
    with open("run.err", "w") as err_file:
        sys.stderr = err_file
        if python_exit_status != 0:
            sys.stderr.write(f"Error occurred while running {python_script}\n")


    if python_exit_status == 0:
        open("RELION_JOB_EXIT_SUCCESS", "w").close()
    else:
        open("RELION_JOB_EXIT_FAILURE", "w").close()

    sys.exit(0)

if __name__ == '__main__':
    main()
