import sys
import operator

if len(sys.argv) != 3:
  print("!!Usage: python get_nbest_word.py arpa_path N")
  sys.exit(1)


file_name = sys.argv[1]
N = int(sys.argv[2])
if N == 0:
  print("N is zero so nothing to compute.")
  sys.exit(0)
elif N < 0:
  N *= -1
  reverse = True

state=0
x = dict()
with open(file_name) as f:
  for line in f:
    line = line.strip()

    if state == 1:
      if len(line) == 0 or line.startswith("\\2-grams:"):
        break
      prob=line.split("\t")[0]
      word=line.split("\t")[1]
      x[word] = prob
    elif state == 0 and line.startswith("\\1-grams:"):
      state=1

sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=reverse)
for i, ngram in enumerate(sorted_x):
  print(ngram[0])
  if i == N - 1:
    break
