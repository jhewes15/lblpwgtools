#!/bin/bash

# Get the script execution directory
export EXEC_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make sure GLoBES is set up
GLB_PATH=$(echo $(which globes))
if [ "${GLB_PATH}" = "" ]; then
  echo "You must have GLoBES in your path to run this script! Exiting..."
  exit 1
fi

# Make sure MGT is set up
MGT_PATH=$(echo $(which mgt))
if [ "${MGT_PATH}" = "" ]; then
  echo "You must have MGT in your path to run! Exiting..."
  exit 1
fi

# Define usage
usage="
Usage: $(basename "$0")  -- Script to submit jobs which run studies using My GLoBES Tools

    OPTIONS:

      REQUIRED
        -n            Name of flux type
                        (used for naming generated flux files)
        -f            FHC flux file
                        (requires full path + filename)
        -r            RHC flux file
                        (requires full path + filename)

      OPTIONAL
        -h            Show this help page.
        -p <params>   Set oscillation parameters to a specified value.
                          <params> takes the form THETA_12,THETA_13,THETA_23,dm^2,DM^2,DCP
                          separated by commas with no spaces in between.
                          FOR EXAMPLE: -p 0.5883,0.1536,0.7222,0.0000754,0.00243,0
        -e <params>   Set fractional errors on oscillation parameters.
                          Syntax is the same as for -p.
        -s <num>      Run specific sensitivity study. Options are:
                          1 = CP violation sensitivity vs delta-cp
                          2 = Mass hierarchy sensitivity vs delta-cp
                          3 = delta-cp resolution vs delta-cp
                          4 = CP violation sensitivity vs exposure
                          5 = Mass hierarchy sensitivity vs exposure
        -t            Test run - disables oscillation parameter systematics.
        -l <num>      Resolution - specifies number of data points for exposure studies.
        -x <num>      X range - specifies maximum exposure for exposure studies
"

# Parse input arguments
optional_args=""

while getopts "n:f:r:hp:e:s:tr:x:" option; do
  case "${option}" in
    n)  flux_name=${OPTARG}
        ;;
    f)  flux_fhc=${OPTARG}
        ;;
    r)  flux_rhc=${OPTARG}
        ;;
    h)  echo "${usage}"
        exit
        ;;
    p)  optional_args="${optional_args} -p ${OPTARG}"
        ;;
    e)  optional_args="${optional_args} -e ${OPTARG}"
        ;;
    s)  if [ "${OPTARG}" -eq "1" ]; then
          optional_args="${optional_args} -C1 -T1"
        elif [ "${OPTARG}" = "2" ]; then
          optional_args="${optional_args} -C1 -T7"
        elif [ "${OPTARG}" -eq "3" ]; then
          optional_args="${optional_args} -C1 -T9"
        elif [ "${OPTARG}" -eq "4" ]; then
          optional_args="${optional_args} -C2 -T4"
        elif [ "${OPTARG}" -eq "5" ]; then
          optional_args="${optional_args} -C2 -T7"
        else
          echo "Invalid run type chosen! Exiting..."
        fi
        ;;
    t)  optional_args="${optional_args} -t"
        ;;
    l)  optional_args="${optional_args} -r ${OPTARG}"
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

if [ -z "${flux_name}" ]; then
  echo
  echo "Flux name not set!"
  echo "${usage}"
  echo "Exiting..."
  exit 1
elif [ -z "${flux_fhc}" ]; then
  echo
  echo "FHC flux file not set!"
  echo "${usage}"
  echo "Exiting..."
  exit 1
elif [ -z "${flux_rhc}" ]; then
  echo
  echo "RHC flux file not set!"
  echo "${usage}"
  echo "Exiting..."
  exit 1
fi

python ${EXEC_PATH}/backend/WriteConfig.py ${flux_name} ${flux_fhc} ${flux_rhc}

mgt ${optional_args} ${EXEC_PATH}/configs/${flux_name}.glb ${EXEC_PATH}/out/${flux_name}.dat

