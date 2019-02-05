import sys

if len(sys.argv) < 3:
   print("!!Usage: python dic2lex.py [pronunciation dictionary] [WFST name]")
   sys.exit(1)

lp = open("WFST/%s/lexiconp.txt"%sys.argv[2],"w")
with open(sys.argv[1]) as f:
    for line in f:
        part = line.strip().split("\t")
        lp.write("%s\t1.0\t%s\n"%(part[0], part[1]))
