#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: ./01PrepLat.sh [Name of UTT] [Nbest]"
  exit
fi

. path.sh

NAME=$1
NBEST=$2
python ../../src/lattice/VecSeq2Lattice.py ${NAME}.npy ${NBEST}
lattice-minimize ark,t:${NAME}.lat.txt ark:- | \
lattice-determinize-pruned ark:- ark:${NAME}.lat.bin
