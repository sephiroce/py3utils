"""

    build up word[tab]bpe pair

Usage:
    python3 PairOfWordBPE.py [bpe corpus]

"""
import sys

if len(sys.argv) < 2:
  print("!!Usage: python3 PairOfWordBPE.py [bpe corpus]")
  sys.exit(1)

VOCAB = None
if len(sys.argv) == 3:
  VOCAB = set(line.strip() for line in open(sys.argv[2]))
  print("Vocab limited to %d"%len(VOCAB))
WORDS = set()
DIC = open("%s.dic" % sys.argv[1], "w")
with open(sys.argv[1]) as f:
  for bpe_line in f:
    bpes = bpe_line.strip().split(" ")

    partial = ""
    for bpe in bpes:
      if "@@" in bpe:
        partial += bpe + " "
        continue
      if partial != "":
        bpe = partial + bpe
        partial = ""
        word = bpe.replace("@@", " ")
      else:
        word = bpe

      if word in WORDS:
        continue
      elif VOCAB and word in VOCAB:
        continue
      else:
        WORDS.add(word)
        line = '%s\t%s' % (word.replace(" ",""), bpe)
        DIC.write(line + "\n")
