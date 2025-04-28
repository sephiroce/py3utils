"""
  This is a wrapping class of arpa library(https://github.com/sfischer13/python-arpa)
  for calculating probabilites of streaming inputs.

  TO-DO
  "arpa" library is too slow to load several GB size LMs.
  Rebuilding KMArpa just for loading and looking up prob for a given word sequence.
  words.txt will be required every time.

  @author: Kyungmin Lee(sephiroce@snu.ac.kr)

  """
import arpa
"""

  The usage of arpa library

import arpa  # Python 3.4+
# OR
import arpa_backport as arpa  # Python 2.7

models = arpa.loadf("foo.arpa")
lm = models[0]  # ARPA files may contain several models.

# probability p(end|in, the)
lm.p("in the end")
lm.log_p("in the end")

# sentence score w/ sentence markers
lm.s("This is the end .")
lm.log_s("This is the end .")

# sentence score w/o sentence markers
lm.s("This is the end .", sos=False, eos=False)
lm.log_s("This is the end .", sos=False, eos=False)
  """

import copy
import math
import numpy as np
import sys

class arpa_wrapper:
  def __init__(self, ngram, vocab = None, base = np.exp(1)):
    self.lm = arpa.loadf(ngram)[0]
    self.base = base
    with open(ngram) as f:
      for line in f:
        if line.startswith("\\1-grams:"):
          break
        if line.startswith("ngram "):
          self.n = int(line.replace("ngram ","").split("=")[0])
    self.context = "<s>"
    self.vocab = None
    is_first_line = True
    is_subword_nmt = True
    if vocab :
      self.vocab = list()
      with open(vocab) as f:
        for line in f:
          w = line.strip()
          if is_first_line :
            is_first_line = False
            if w is "{":
              is_subword_nmt = True
              continue
            else:
              is_subword_nmt = False

          if is_subword_nmt:
            if w is "}":
              break
            else:
              p=w.split(": ")
              v=p[0][1:len(p[0])-1]
              i=int(p[1][0:len(p[1])-1])
              if v == "<s>":
                continue
              else:
                self.vocab.append(v)
                if self.vocab[i] is not v:
                    print("Wrong word index!! index: %d vocab in the file: %s vocab in the list: %s"%(i,v,self.vocab[i]))
          else:
            self.vocab.append(w.split("\t")[0].split(" ")[0].strip())
      print("%d vocabs were loaded for shallow fusion w/ arpa"%len(self.vocab))
  
  def add_word_to_context(self, word):
#    if len(self.context) == self.n:
#      self.context.pop(0)

#    self.context.append(word)
    self.context += " " + word

  # return softmax of n-gram
  def dist(self):
    if not self.vocab :
      print("Please input word.txt")
      return None

    probs = list()
    probs_final = None
    sum_prob = 0
    sum_prob_final = 0
    print(self.context)
    for v in self.vocab:
      cur_ngram = self.context +" " + v
      p = self.lm.p(cur_ngram)
#      p = math.log(pp, 10)
#      print("%s %.5f"%(cur_ngram,p))
      probs.append(p)
      sum_prob += p
    
    out= np.divide(np.array(probs), sum_prob)
    print("%s %.7f"%(self.vocab[np.argmax(out)],out[np.argmax(out)] ))
    print("%s %.7f"%(self.vocab[np.argmin(out)],out[np.argmin(out)] ))
    return out
  
  def clean(self):
    self.context="<s>"
