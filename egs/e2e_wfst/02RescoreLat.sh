#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: ./02RescoreLat.sh [Name of UTT] [WFST] [LM]"
  exit
fi

. path.sh

NAME=$1
WFST=$2
LM=$3
lattice-compose ark:${NAME}.lat.bin ${WFST} ark:- | \
lattice-lmrescore --lm-scale=-1.0 ark:- "fstproject --project_output=true ${LM}|" ark:${NAME}.res.lat.bin
