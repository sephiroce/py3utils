# A sequence of vectors to Lattice
- It converts a sequence of vectors which have the same dimension to a lattice.

## Usage
- Input1 - Matrix(A sequence of vectors) composed of real numbers in numpy text format.
- Input2 - n-best (default = 3)
- Output - The Kaldi lattice.

"""
> python VecSeq2Lattice.py In: matrix In: n-best Out: name of lattice
ex) > python VecSeq2Lattice.py vec.npy 3 vec.lat
"""


