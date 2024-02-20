#!/bin/bash

current_dir=$(dirname "$(realpath "$0")")
root_dir=$(realpath "$current_dir/../")
export PYTHONPATH=$root_dir

# Define functions
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --in_mics|-in_mics)
                in_mics="$2"
                shift 2
                ;;
            --o)
                out_dir="$2"
                shift 2
                ;;
            --r_min|-resolution_min)
                resolution_min="$2"
                shift 2
                ;;
            --r_max|-resolution_max)
                resolution_max="$2"
                shift 2
                ;;
            --j|-nr_threads)
                nr_threads="$2"
                shift 2
                ;;
            *)
                echo "Invalid option: $1"
                exit 1
                ;;
        esac
    done

    if [[ -z $in_mics || -z $out_dir || -z $resolution_min || -z $resolution_max || -z $nr_threads ]]; then
        echo "Usage: $0 --in_mics <input_tilts_file> --o <output_directory> --r_min <resolution_min> --r_max <resolution_max> --j <nr_threads>"
        exit 1
    fi
}

main() {
    # Parse arguments
    parse_arguments "$@"

    # Execute the Python script
    python3 "$root_dir/src/lib/exclude_tilts/exclude_tilts_rules_bit.py" --i "$in_mics" --o "$out_dir" --r_min "$resolution_min" --r_max "$resolution_max" --j "$nr_threads"
    python_exit_status=$?

    # Redirect stdout and stderr to files
    cd "$out_dir" || exit

    {
        echo "" > run.out
        echo "" > run.err
    } || {
        echo "Error writing to files."
        exit 1
    }

    # Write to RELION_JOB_EXIT_SUCCESS upon successful exit
    if [[ $python_exit_status -eq 0 ]]; then
        touch RELION_JOB_EXIT_SUCCESS
    else
        # Write to RELION_JOB_EXIT_FAILURE upon failure
        touch RELION_JOB_EXIT_FAILURE
    fi

    exit 0

}

# Execute main function
main "$@"


