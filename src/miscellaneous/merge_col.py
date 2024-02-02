import sys

if len(sys.argv) < 4:
  print("!!Usage : python merge_col.py a b c")
  sys.exit(1)

a = open(sys.argv[1]).readlines()
b = open(sys.argv[2]).readlines()
c = open(sys.argv[3],"w")

for i, line in enumerate(a):
  c.write("%s\t%s\n"%(line.strip(),b[i].strip()))

