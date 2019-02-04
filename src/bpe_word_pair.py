"""

    build up bpe[tab]word pair

Usage:
    python3 bpe_word_pair.py [bpe corpus]

"""
import sys

if len(sys.argv) < 2:
  print("!!Usage: python3 bpe_word_pair.py [bpe corpus]")
  sys.exit(1)

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
      else:
        WORDS.add(word)
        line = '%s\t%s' % (bpe, word.replace(" ",""))
        DIC.write(line + "\n")
