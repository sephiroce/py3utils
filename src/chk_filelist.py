#!/usr/bin/python3
import sys
from pathlib import Path

line_n = 0
missing_n = 0
with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip()
		if len(line) == 0 :
			continue
		line_n += 1
		my_file = Path(line)
		if not my_file.exists():
			missing_n += 1
			print("%s doesn't exist!"%line)
print("Total %d files, %d files are missing."%(line_n, missing_n))

