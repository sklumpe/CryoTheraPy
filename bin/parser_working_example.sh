#!/bin/bash

# Define paths
current_dir=$(dirname "$(realpath "$0")")
root_dir=$(realpath "$current_dir/../")
export PYTHONPATH=$root_dir

# Parse command-line arguments
while getopts ":i:o:" opt; do
  case $opt in
    i) in_tilts="$OPTARG"
    ;;
    o) out_dir="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

# Check if required arguments are provided
if [ -z "$in_tilts" ] || [ -z "$out_dir" ]; then
  echo "Usage: $0 --i <input_tilts_file> --o <output_directory>"
  exit 1
fi

# Execute the Python script with command-line arguments
python3 "$root_dir/src/lib/exclude_tilts/working_example.py" --i "$in_tilts" --o "$out_dir"
python_exit_status=$?

# Change the working directory to the output directory
cd "$out_dir" || exit

# Write to RELION_JOB_EXIT_SUCCESS upon successful exit
if [ $python_exit_status -eq 0 ]; then
  touch RELION_JOB_EXIT_SUCCESS
else
  touch RELION_JOB_EXIT_FAILURE
fi

# Redirect stdout and stderr to files
{
  echo "" > run.out
  echo "" > run.err
} || {
  echo "Error writing to files."
  exit 1
}

exit 0
