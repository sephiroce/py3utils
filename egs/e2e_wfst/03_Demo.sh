#!/bin/bash

python DummyNPArr.py
#rm -rf WFST
./00_Building_WFST.sh data Librispeech-10k
./01_decode.sh UTT0001 2 Librispeech-10k
