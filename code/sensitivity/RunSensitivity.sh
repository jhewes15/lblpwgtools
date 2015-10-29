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
        -N            Name of flux type
                        (used for naming generated flux files)
        -F            FHC flux file
                        (requires full path + filename)
        -R            RHC flux file
                        (requires full path + filename)

      OPTIONAL
        -h            Show this help page.
        -o <params>   Set oscillation parameters to a specified value.
                          <params> takes the form THETA_12,THETA_13_NH,THETA_13_IH,THETA_23_NH,THETA_23_IH,dm^2,DM^2_NH,DM^2_IH,DCP
                          separated by commas with no spaces in between.
                          FOR EXAMPLE: -p 0.5883,0.1536,0.1555,0.7222,0.7202,0.0000754,0.00243,-0.00238,0
        -e <params>   Set fractional errors on oscillation parameters.
                          Syntax is the same as for -o.
        -g            Submit jobs to the grid.
        -n,i          Specify normal hierarchy only (n) or inverted hierarchy only (i). Default is both.
        -t            Test run - disables oscillation parameter systematics.
        -r <num>      Resolution - specifies number of data points for exposure studies.
        -x <num>      X range - specifies maximum exposure for exposure studies
        -1,2,3,4,5    Run specific sensitivity study. Options are:
                          1 = CP violation sensitivity vs delta-cp
                          2 = Mass hierarchy sensitivity vs delta-cp
                          3 = delta-cp resolution vs delta-cp
                          4 = CP violation sensitivity vs exposure
                          5 = Mass hierarchy sensitivity vs exposure
                          Can specify multiple options, defaults to all.
"

# Parse input arguments
usegrid=0
resolution=0
xrange=0
osc_syst=1
both_hierarchies=1
which_hierarchy=2
parallelise=0
plot=0

while getopts "N:F:R:O:ho:e:gnitr:x:12345" option; do
  case "${option}" in
    N)  flux_name=${OPTARG}
        ;;
    F)  flux_fhc=${OPTARG}
        ;;
    R)  flux_rhc=${OPTARG}
        ;;
    O)  out_file=${OPTARG}
        ;;
    h)  echo "${usage}"
        exit
        ;;
    o)  params=${OPTARG}
        ;;
    e)  errors=${OPTARG}
        ;;
    g)  if [ "${plot}" -eq "0" ]; then
          usegrid=1
        else
          echo You have selected the -q option, so jobs will not be submitted to the grid.
        fi
        ;;
    n)  if [ "${both_hierarchies}" -eq "0" ]; then
          echo Hierarchy specified more than once! Exiting...
          exit
        fi
        echo Running for normal hierarchy only...
        both_hierarchies=0
        which_hierarchy=0
        ;;
    i)  if [ "${both_hierarchies}" -eq "0" ]; then
          echo Hierarchy specified more than once! Exiting...
          exit
        fi
        echo Running for inverted hierarchy only...
        both_hierarchies=0
        which_hierarchy=1
        ;;
    t)  echo Oscillation parameter systematics disabled.
        osc_syst=0
        ;;
    r)  resolution=${OPTARG}
        echo Resolution for exposure plots set to ${resolution}
        ;;
    x)  xrange=${OPTARG}
        echo Maximum exposure for exposure plots set to ${xrange}
        ;;
    1)  echo Study enabled:    CP violation sensitivity vs delta-cp
        studies="${studies} 0"
        ;;
    2)  echo Study enabled:    Mass hierarchy sensitivity vs delta-cp
        studies="${studies} 1"
        ;;
    3)  echo Study enabled:    delta-cp resolution vs delta-cp
        studies="${studies} 2"
        ;;
    4)  echo Study enabled:    CP violation sensitivity vs exposure
        studies="${studies} 3"
        ;;
    5)  echo Study enabled:    Mass hierarchy sensitivity vs exposure
        studies="${studies} 4"
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
elif [ -z "${out_file}" ]; then
  echo
  echo "Output file not set!"
  echo "${usage}"
  echo "Exiting..."
  exit 1
fi

python ${EXEC_PATH}/backend/WriteConfig.py ${flux_name} ${flux_fhc} ${flux_rhc}

mgt -C1 -T1 ${EXEC_PATH}/configs/${flux_name}.glb ${out_file}

