"""
sample sentence: cindy jean
  p( cindy | <s> )  = [1gram] 0.09876432 [ -1.0054 ]
  p( jean | cindy ...)  = [2gram] 0.5555204 [ -0.2553 ]
  p( </s> | jean ...)   = [2gram] 0.2777794 [ -0.5563 ]
1 sentences, 2 words, 0 OOVs
0 zeroprobs, logprob= -1.817 ppl= 4.033357 ppl1= 8.100279

file sample.txt: 1 sentences, 2 words, 0 OOVs
0 zeroprobs, logprob= -1.817 ppl= 4.033357 ppl1= 8.100279
"""

"""
\data\
ngram 1=7
ngram 2=7

\1-grams:
-1.0000 <unk>	-0.2553
-98.9366 <s>	 -0.3064
-1.0000 </s>	 0.0000
-0.6990 wood	 -0.2553
-0.6990 cindy	-0.2553
-0.6990 pittsburgh		-0.2553
-0.6990 jean	 -0.1973

\2-grams:
-0.2553 <unk> wood
-0.2553 <s> <unk>
-0.2553 wood pittsburgh
-0.2553 cindy jean
-0.2553 pittsburgh cindy
-0.5563 jean </s>
-0.5563 jean wood 

\end\
"""

import sys
from arpa_wrapper import arpa_wrapper
if len(sys.argv) < 3:
  print("!!USAGE: python arpa_wrapper_test.py [arpa] \"[sample sentence]\" (optinally)words.txt")
  sys.exit(1)
aw = None
if len(sys.argv) == 4:
  aw = arpa_wrapper(sys.argv[1], sys.argv[3])
else:
  aw = arpa_wrapper(sys.argv[1])
print("Model has been loaded")
words = sys.argv[2].strip().split(" ")
prob = 0

for i, word in enumerate(words):
  if i == len(words) - 1 :
    prob += aw.prob(word,True)
  else :
    prob += aw.prob(word)

print("%.5f"%prob)

for i ,word in enumerate(words):
  print(aw.dist())
  aw.add_word_to_context(word)

print(aw.dist(True))
