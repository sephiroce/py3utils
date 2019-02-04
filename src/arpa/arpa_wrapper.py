"""
  This is a wrapping class of arpa library(https://github.com/sfischer13/python-arpa)
  for calculating probabilites of streaming inputs.

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

import math
import sys

class arpa_wrapper:
  def __init__(self, ngram):
    self.lm = arpa.loadf(ngram)[0]
    with open(ngram) as f:
      for line in f:
        if line.startswith("\\1-grams:"):
          break
        if line.startswith("ngram "):
          self.n = int(line.replace("ngram ","").split("=")[0])
    self.words=["<s>"]
  
  def _get_word_seq(self, word):
    self.words.append(word)
    if len(self.words) == self.n + 1:
      self.words.pop(0)
    
    word_seq = ""
    for i in range(len(self.words)):
      word_seq += self.words[i] +" "
    return word_seq.strip()

  def prob(self, word, is_final=False):
    word_seq = self._get_word_seq(word)
    if is_final:
      p1 = math.log(self.lm.p(word_seq),10)
      final_word_seq = self._get_word_seq("</s>")
      p2 = math.log(self.lm.p(final_word_seq), 10)
      self.clean()
      return p1 + p2
    else:
      return math.log(self.lm.p(word_seq),10)
  def clean(self):
    self.words=["<s>"]

