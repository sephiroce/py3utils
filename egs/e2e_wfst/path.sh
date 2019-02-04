#!/bin/bash
KALDI=../../tools/kaldi
OPENFST=${KALDI}/tools/openfst
export PATH=${KALDI}/src/bin:${KALDI}/src/chainbin:${KALDI}/src/featbin:${KALDI}/src/fgmmbin:${KALDI}/src/fstbin:${KALDI}/src/gmmbin:${KALDI}/src/ivectorbin:${KALDI}/src/kwsbin:${KALDI}/src/latbin:${KALDI}/src/lmbin:${KALDI}/src/nnet2bin:${KALDI}/src/nnet3bin:${KALDI}/src/nnetbin:${KALDI}/src/online2bin:${KALDI}/src/onlinebin:${KALDI}/src/rnnlmbin:${KALDI}/src/sgmm2bin:${KALDI}/src/tfrnnlmbin:${OPENFST}/src/bin:${PATH}
