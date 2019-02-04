#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: ./00BuildWFST.sh [lexicon] [word-sym-table] [bpe-sym-table]"
  exit
fi

. path.sh

DICT=${1}
WORD=${2}
BPES=${3}

