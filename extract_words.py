#!/bin/python3
import sys

if len(sys.argv) is not 1:
	print("!!Usage: python3 extract_words.py in:text")
	sys.exit(1)

words=set()
with open(sys.argv[1]) as f:
	for line in f:
		words_in_line=line.split(" ")
		for word in words_in_line:
			words.add(word)
for word in words:
	print(word)
