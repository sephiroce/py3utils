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
    self.context = ["<s>"]
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
  
  def _get_context(self):
    if len(self.context) == self.n:
      self.context.pop(0)

    context = ""
    for i in range(len(self.context)):
      context += self.context[i] + " "
    return context

  def prob(self, word, is_final=False):
    context = self._get_context()
    print(context + word)
    p1 = math.log(self.lm.p(context + word), self.base)
    self.context.append(word)
    p2 = 0.0
    if is_final:
      context = self._get_context()
      print(context + "</s>")
      p2 = math.log(self.lm.p(context + "</s>"), self.base)
      self.clean()
    return p1 + p2

  def add_word_to_context(self, word):
    if len(self.context) == self.n:
      self.context.pop(0)

    self.context.append(word)

  # return softmax of n-gram
  def dist(self, is_final = False):
    if not self.vocab :
      print("Please input word.txt")
      return None

    context = self._get_context()
    probs = list()
    probs_final = None
    sum_prob = 0
    sum_prob_final = 0
    for v in self.vocab:
      cur_ngram = context + v
      p = math.log(self.lm.p(cur_ngram), self.base)
      probs.append(p)
      sum_prob += p
      if is_final:
        probs_final = list()
        new_ngram_arr = cur_ngram.split(" ")
        if len(new_ngram_arr) == self.n:
          new_ngram_arr.pop(0)
        new_context = ""
        for word in new_ngram_arr:
          new_context += word + " "
        p = math.log(self.lm.p(new_context + "</s>"), self.base)
        probs_final.append(p)
        sum_prob_final += p

    if is_final:
      self.clean()
      return np.divide(np.array(probs),sum_prob) + \
          np.divide(np.array(probs_final), sum_prob_final)
    return np.divide(np.array(probs), sum_prob)
  
  def clean(self):
    self.context=["<s>"]

