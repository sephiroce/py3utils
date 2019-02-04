#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: ./03BestPath.sh [Name of UTT] [Word symbol table]"
  exit
fi

. path.sh

NAME=$1
SYMS=$2
lattice-best-path ark:${NAME}.res.lat "ark,t:|${KALDI}/egs/wsj/s5/utils/int2sym.pl -f 2- ${SYMS} > ${NAME}.utt" ark:${NAME}.ali
