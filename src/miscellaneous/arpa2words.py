#!/usr/local/bin/python3

import sys

if len(sys.argv) < 2:
    print("Usage: ./arpa2words.py arpa")
    sys.exit(1)

if not sys.argv[1].endswith(".arpa"):
    print("The file extension of ARPA format files is \"arpa\"")
    sys.exit(2)

name=sys.argv[1].replace(".arpa","")
fw = open("%s.words"%name, "w")
status = 0
ExpectedWords = 0
ActuallyWords = 0
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if status == 1:
            if ExpectedWords ==0:
                print("Expected Words is ZERO!")
                sys.exit(3)
            if len(line) == 0:
                break
            else:
                fw.write("%s\n"%line.split("\t")[1])
                ActuallyWords += 1
        else:
            if line == "\\1-grams:":
                status = 1
            elif line.startswith("ngram 1="):
                ExpectedWords = int(line.split("=")[1])

if ExpectedWords == ActuallyWords:
    print("Sucessfully %d words were extracted and saved to %s.words"%(ExpectedWords, name))
else:
    print("WARNNING: The number of expected words is %d but the given arpa contains %d words. "\
          + "Anyway the words file was saved to %s.words"%(ExpectedWords, ActuallyWords, name))

