#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: ./decode.sh [Name of UTT] [Nbest] [WFST]"
  exit
fi

. path.sh

UTT_ID=$1
NBEST=$2
WFST=$3

python ../../src/lattice/VecSeq2WFST.py ${UTT_ID}.npy ${NBEST}

fstcompile ${UTT_ID}.fst.txt | fstminimize | fstarcsort --sort_type=olabel > ${UTT_ID}.fst.bin

fstcompose WFST/${WFST}/BG.fst ${UTT_ID}.fst.bin | \
  fstdeterminizestar --use-log=true | \
  fstminimizeencoded | fstpushspecial | \
  fstarcsort | fstproject > ${UTT_ID}.fst.res.bin

echo ${UTT_ID} > ${UTT_ID}.lat.res.txt
fstprint ${UTT_ID}.fst.res.bin | python utils/fst2lat.py >> ${UTT_ID}.lat.res.txt

lattice-best-path --acoustic-scale=1 --word-symbol-table=data/${WFST}.words ark,t:${UTT_ID}.lat.res.txt
