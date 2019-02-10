#!/usr/local/bin/python3

import sys

if len(sys.argv) < 2:
    print("Usage: ./apo2dqo.py [bpe corpus]")
    sys.exit(1)

if not sys.argv[1].endswith(".bpe"):
    print("The file extension of bpe text files is \"bpe\"")
    sys.exit(2)

name=sys.argv[1].replace(".bpe","")
fw = open("%s.dqo.bpe"%name, "w")
with open(sys.argv[1]) as f:
    for line in f:
        words = line.strip().split(" ")
        for i, word in enumerate(words):
            if "'" in word:
                word = word.replace("'","")
                word = "\"%s\""%word
            if i == len(words) - 1:
                fw.write("%s\n"%word)
            else:
                fw.write("%s "%word)
    
print("Saved to %s.dqo.bpe"%(name))

