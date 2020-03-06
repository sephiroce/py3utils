import sys

if len(sys.argv) != 3:
  print("!!Usage: python get_line_contains_word.py word_list text")
  sys.exit(1)

#word: line1, line2

word_set = set()
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    word_set.add(line)

oov_file = open(sys.argv[2]+".oov", "w")
inv_file = open(sys.argv[2]+".inv", "w")
with open(sys.argv[2]) as f:
  for line in f:
    line = line.strip()
    is_contain = False
    for word in line.split(" "):
      if word in word_set:
        oov_file.write(line+"\n")
        is_contain = True 
        break
    if not is_contain:
        inv_file.write(line+"\n")

oov_file.close()
inv_file.close()
