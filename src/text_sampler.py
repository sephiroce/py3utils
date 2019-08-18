import sys
import random

total_line = sys.argv[1]
mix_list_path = sys.argv[2]
mix_lines = dict()
dest_file = open(mix_list_path+".txt", "w")
with open(mix_list_path) as mix_file:
  for line in mix_file:
    line = line.strip()
    mix_lines[line.split()[0]] = int(line.split()[1] * total_line)

for file_name in mix_lines:
  line_num = 0
  with open(file_name) as text_file:
    for line in text_file.readlines():
      line_num += 1

  line_list = random.sample(range(line_num), mix_lines[file_name])

  with open(file_name) as text_file:
    for i, line in enumerate(text_file.readlines()):
      if i in line_list:
        dest_file.write(line+"\n")

dest_file.close()
