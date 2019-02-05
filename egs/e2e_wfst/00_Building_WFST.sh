#!/bin/bash

. path.sh

if [ "$#" -ne 2 ]; then
    echo "!!Usage: ./BuildWFST.sh BASE_PATH NAME"
    exit 1;
fi

BASE_PATH=${1}
WFST=${2}
LMFile=${BASE_PATH}/${2}.arpa
word_syms=${BASE_PATH}/${WFST}.words
DIC=${BASE_PATH}/${WFST}.dic
BPES=${BASE_PATH}/${WFST}.bpes

if [ ! -f $LMFile ] || [ ! -f $word_syms ] || [ ! -f $DIC ] || [ ! -f $BPES ]; then
    ls $LMFile
    ls $word_syms
    ls $DIC
    ls $BPES
    exit 1;
fi

mkdir -p WFST/${WFST}
cp ${word_syms} WFST/${WFST}/words.txt

# Build G-WFST using a given language model
if [ -f WFST/${WFST}/G.fst ]; then
  echo WFST/${WFST}/G.fst exists.
else
  cat ${LMFile} | utils/find_arpa_oovs.pl ${word_syms} > WFST/${WFST}/oov.txt
    arpa2fst --read-symbol-table=${word_syms} --disambig-symbol=#0 \
            ${LMFile} | fstdeterminizestar --use-log=true  | \
            fstminimizeencoded | fstpushspecial | \
            fstarcsort > WFST/${WFST}/G.fst
    fstisstochastic WFST/${WFST}/G.fst
    echo WFST/${WFST}/G.fst was built.
fi

#Preparing bpes.txt
if [ -f WFST/${WFST}/lexiconp.txt ]; then
    echo WFST/${WFST}/lexiconp.txt exists.
else
    #dic2lex.py makes WFST/${WFST}/lexiconp.txt
    python3 utils/dic2lex.py ${DIC} ${WFST}
    echo WFST/${WFST}/lexiconp.txt was built.
fi

if [ -f WFST/${WFST}/bpes.txt ]; then
    echo WFST/${WFST}/bpes.txt exists.
else
    # Build B_disambig-WFST using a given lexicon
    ndisambig=`utils/add_lex_disambig.pl --pron-probs WFST/${WFST}/lexiconp.txt WFST/${WFST}/BPE_disambig.txt`
    ndisambig=$[$ndisambig+1]; # add one disambig symbol for silence in lexicon FST

    # Format of BPE_disambig.txt:
    # !SIL  1.0   SIL_S
    # <SPOKEN_NOISE>    1.0   SPN_S #1
    # <UNK> 1.0  SPN_S #2
    # <NOISE>   1.0  NSN_S
    # !EXCLAMATION-POINT    1.0  EH2_B K_I S_I K_I L_I AH0_I M_I EY1_I SH_I AH0_I N_I P_I OY2_I N_I T_E
    ( for n in `seq 0 $ndisambig`; do echo '#'$n; done ) > WFST/${WFST}/disambig.txt

    # Create bpe symbol table
    grep -v '#' ${BPES} | cat - WFST/${WFST}/disambig.txt | awk '{n=NR-1; print $1, n;}' > WFST/${WFST}/bpes.txt
    echo WFST/${WFST}/bpes.txt was built.
fi

# Build B-WFST using a given lexicon
sil_prob=0.5
silphone="</s>"

if [ -f WFST/${WFST}/B.fst ]; then
    echo WFST/${WFST}/B.fst exists.
else
    python3 utils/make_lexicon_fst.py --sil-prob=$sil_prob --sil-phone=$silphone \
            WFST/${WFST}/lexiconp.txt | \
    fstcompile --isymbols=WFST/${WFST}/bpes.txt --osymbols=WFST/${WFST}/words.txt \
      --keep_isymbols=false --keep_osymbols=false | \
    fstarcsort --sort_type=olabel > WFST/${WFST}/B.fst || exit 2;
    echo WFST/${WFST}/B.fst was built.
fi

if [ -f WFST/${WFST}/B_disambig.fst ]; then
    echo WFST/${WFST}/B_disambig.fst exists.
else
    bpe_disambig_symbol=`grep \#0 WFST/${WFST}/bpes.txt | awk '{print $2}'`
    word_disambig_symbol=`grep \#0 WFST/${WFST}/words.txt | awk '{print $2}'`
    python3 utils/make_lexicon_fst.py \
        --sil-prob=$sil_prob --sil-phone=$silphone --sil-disambig='#'$ndisambig \
        WFST/${WFST}/BPE_disambig.txt | \
        fstcompile --isymbols=WFST/${WFST}/bpes.txt --osymbols=WFST/${WFST}/words.txt \
        --keep_isymbols=false --keep_osymbols=false | \
        fstaddselfloops "echo $bpe_disambig_symbol |" "echo $word_disambig_symbol |" | \
        fstarcsort --sort_type=olabel > WFST/${WFST}/B_disambig.fst || exit 2;
    echo WFST/${WFST}/B_disambig.fst was built.
fi

# Compose G.fst and B.fst
fsttablecompose WFST/${WFST}/B_disambig.fst WFST/${WFST}/G.fst | \
    fstdeterminizestar --use-log=true | fstminimizeencoded | fstpushspecial | \
     fstarcsort > WFST/${WFST}/BG.fst

