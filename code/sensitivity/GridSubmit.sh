#!/bin/bash

# Get the script execution directory
export EXEC_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define usage
usage="
Usage: $(basename "$0")  -- Submit grid jobs to run sensitivity studies

    OPTIONS:

      REQUIRED
        -n            Name of input file
                        (found under flux_inputs/<name>.txt
        -o <dir>      Output directory
                        (should be in /lbne/data/users/you to prevent errors)
        -s <num>      Run specific sensitivity study. Options are:
                          1 = CP violation sensitivity vs delta-cp
                          2 = Mass hierarchy sensitivity vs delta-cp
                          3 = delta-cp resolution vs delta-cp
                          4 = CP violation sensitivity vs exposure
                          5 = Mass hierarchy sensitivity vs exposure

      OPTIONAL
        -h            Show this help page.
        -p <params>   Set oscillation parameters to a specified value.
                          <params> takes the form THETA_12,THETA_13,THETA_23,dm^2,DM^2,DCP
                          separated by commas with no spaces in between.
                          FOR EXAMPLE: -p 0.5883,0.1536,0.7222,0.0000754,0.00243,0
        -e <params>   Set fractional errors on oscillation parameters.
                          Syntax is the same as for -p.
        -t            Test run - disables oscillation parameter systematics.
        -l <num>      Resolution - specifies number of data points for exposure studies.
        -x <num>      X range - specifies maximum exposure for exposure studies
"

# Parse input arguments
optional_args=""

while getopts "n:s:o:hp:e:tr:x:" option; do
  case "${option}" in
    n)  optional_args="${optional_args} -n ${OPTARG}"
        run_name="${OPTARG}"
        ;;
    o)  OUTPUT_PATH=${OPTARG}
        ;;
    s)  optional_args="${optional_args} -s ${OPTARG}"
        ;;
    h)  echo "${usage}"
        exit
        ;;
    p)  optional_args="${optional_args} -p ${OPTARG}"
        ;;
    e)  optional_args="${optional_args} -e ${OPTARG}"
        ;;
    t)  optional_args="${optional_args} -t"
        ;;
    l)  optional_args="${optional_args} -l ${OPTARG}"
        ;;
    x)  optional_args="${optional_args} -x ${OPTARG}"
        ;;
    :)  printf "missing argument for -%s\n" "$OPTARG" >&2
        echo "$usage" >&2
        exit 1
        ;;
    \?) printf "illegal option: -%s\n" "$OPTARG" >&2
        echo "$usage" >&2
        exit 1
        ;;
  esac
done

if [ -z "${run_name}" ]; then
  echo "Input file not set!"
  echo "${usage}"
  echo "Exiting..."
  exit 1
fi

# Get the input list file and count the number of lines

input_file=${EXEC_PATH}/flux_inputs/${run_name}.txt
num_lines=`wc -l < "${input_file}"`

export CONFIG_PATH=${EXEC_PATH}/configs
export FLUX_PATH=${EXEC_PATH}/flux_inputs
export BACKEND_PATH=${EXEC_PATH}/backend
export MGT_PATH=${EXEC_PATH}/../mgt/bin

jobsub_submit -G lbne --OS=SL6 --resource-provides=usage_model=opportunistic -N ${num_lines} -dOUT ${OUTPUT_PATH} -e CONFIG_PATH -e FLUX_PATH -e BACKEND_PATH -e MGT_PATH file://${EXEC_PATH}/backend/GridScript.sh ${optional_args}

# Clean up environment variables
unset CONFIG_PATH
unset FLUX_PATH
unset BACKEND_PATH
unset MGT_PATH
unset EXEC_PATH

