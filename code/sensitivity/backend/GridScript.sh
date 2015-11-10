#!/bin/bash

# Set up some environment
source /grid/fermiapp/products/common/etc/setups.sh
source /grid/fermiapp/larsoft/products/setup
setup jobsub_client v1_0_5
setup ifdhc v1_7_2
setup python v2_7_6
setup gsl v1_16a -q prof

ups list -aK+ gsl

# Parse input arguments
optional_args=""

while getopts "n:p:e:s:tr:x:" option; do
  case "${option}" in
    n)  run_name=${OPTARG}
        ;;
    p)  optional_args="${optional_args} -p ${OPTARG}"
        ;;
    e)  optional_args="${optional_args} -e ${OPTARG}"
        ;;
    s)  if [ "${OPTARG}" -eq "1" ]; then
          optional_args="${optional_args} -C1 -T1"
          study_name="cpsens"
        elif [ "${OPTARG}" = "2" ]; then
          optional_args="${optional_args} -C1 -T7"
          study_name="mhsens"
        elif [ "${OPTARG}" -eq "3" ]; then
          optional_args="${optional_args} -C1 -T9"
          study_name="cpres"
        elif [ "${OPTARG}" -eq "4" ]; then
          optional_args="${optional_args} -C2 -T4"
          study_name="cpexp"
        elif [ "${OPTARG}" -eq "5" ]; then
          optional_args="${optional_args} -C2 -T7"
          study_name="mhexp"
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

# Copy flux list file over
ifdh cp -D ${FLUX_PATH}/${run_name}.txt ${_CONDOR_SCRATCH_DIR}

# Pull out current flux file
line=`sed -n "$((PROCESS+1)) p" ${_CONDOR_SCRATCH_DIR}/${run_name}.txt`
flux_name=`echo ${line} | cut -f1 -d " "`
flux_fhc=`echo ${line} | cut -f2 -d " "`
flux_rhc=`echo ${line} | cut -f3 -d " "`

# Copy over flux files
ifdh cp -D ${flux_fhc} ${_CONDOR_SCRATCH_DIR}
ifdh cp -D ${flux_rhc} ${_CONDOR_SCRATCH_DIR}

flux_fhc="${_CONDOR_SCRATCH_DIR}/${flux_fhc##*/}"
flux_rhc="${_CONDOR_SCRATCH_DIR}/${flux_rhc##*/}"

# Copy over config-writing scripts and core inputs
ifdh cp -D ${BACKEND_PATH}/WriteConfigGrid.py ${_CONDOR_SCRATCH_DIR}
ifdh cp -r ${CONFIG_PATH}/core ${_CONDOR_SCRATCH_DIR}

# Generate GLoBES config file
python ${_CONDOR_SCRATCH_DIR}/WriteConfigGrid.py ${flux_name} ${flux_fhc} ${flux_rhc}

# Run MGT
${MGT_PATH}/mgt ${optional_args} ${_CONDOR_SCRATCH_DIR}/${flux_name}.glb ${CONDOR_DIR_OUT}/${flux_name}_${study_name}.dat

