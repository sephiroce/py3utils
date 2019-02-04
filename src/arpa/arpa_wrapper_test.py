"""
cindy jean
  p( cindy | <s> )  = [1gram] 0.09876432 [ -1.0054 ]
  p( jean | cindy ...)  = [2gram] 0.5555204 [ -0.2553 ]
  p( </s> | jean ...)   = [2gram] 0.2777794 [ -0.5563 ]
1 sentences, 2 words, 0 OOVs
0 zeroprobs, logprob= -1.817 ppl= 4.033357 ppl1= 8.100279

file sample.txt: 1 sentences, 2 words, 0 OOVs
0 zeroprobs, logprob= -1.817 ppl= 4.033357 ppl1= 8.100279
"""

from arpa_wrapper import arpa_wrapper
aw = arpa_wrapper("test.arpa")
print("Sample Text: cindy jean")
print("Probability: %.6f"%(aw.prob("cindy") + aw.prob("jean",True)))
