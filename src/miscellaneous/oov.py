#!/bin/python3
import sys


print ("INFO: This is for vocab of subword-nmt.")

if len(sys.argv) is not 3:
  print("USAGE: python3 oov.py in:vocab_file in:text_corpus")
  sys.exit(1)

# Reading vocab file
vocab=set()
is_subwordnmt = False
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    if line == "{":
      is_subwordnmt = True
      continue
    if line == "}":
      break
    if is_subwordnmt:
      word = line.split(":")[0]
      word = word[1:len(word)-1]
    else:
      word = line.strip()
    vocab.add(word)

print("%d words were loaded"%len(vocab))

# Checking OOV
f_oov = open(sys.argv[2]+".oov","w")
f_unk = open(sys.argv[2]+".oov_processed","w")
index = 0
with open(sys.argv[2]) as f:
  for line in f:
    line = line.strip()
    words = line.split(" ")
    for word in words:
      if word not in vocab:
#        print("OOV: %s"%word)
        f_oov.write("%s\n"%word)
        f_unk.write("<unk> ")
      else:
        f_unk.write("%s "%word)
      index += 1
      if index == len(words):
        f_unk.write("\n")
        index = 0

