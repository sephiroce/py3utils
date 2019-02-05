import numpy as np
import sys


if len(sys.argv) < 3:
  print("USAGE: python VecSeq2Lattice.py uttid.npy nbest")
  sys.exit(1)

nt = np.load(sys.argv[1])
name = sys.argv[1].replace(".npy","")
nb = int(sys.argv[2])
depth = len(nt[0])
if nb > depth:
  print("WARN: nbest should be smaller than the depth of vectors thus nbest is set to %d rather than %d"%(depth,nb))
  nb = depth
Nbest = nb * -1

parents = list()
state = 1
final_state = pow(nb, len(nt) + 1)

print("The name of utterance: %s"%name)
print("Length of the given sequence: %d"%len(nt))
print("Depth of the given sequence: %d"%depth)
latfile = open("%s.fst.txt"%name,"w")
#latfile.write("%s\n"%name)
latfile.write("0 1 0 0 5.0\n")
for t in range(len(nt)):
  P = pow(nb, t)
  for p in range(P):
    for ol in nt[t].argsort()[Nbest:][::-1]:
      state = state + 1
      latfile.write("%d %d %d %d %.6f\n"%(state / nb, state, ol, ol,nt[t][ol]))
      if t == len(nt) - 1:
        latfile.write("%d %d 0 0 5.0\n"%(state, final_state))
latfile.write("%d 5.0\n"%final_state)

