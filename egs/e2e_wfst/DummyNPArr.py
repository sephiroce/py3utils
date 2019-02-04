import numpy as np

data=np.array([[0,2.1,0,1.1, 0],
    [0,0,1.1,2.1,0],
    [0,1.1,2.1,0,0],
    [0,0,2.1,0,0.1]])

outfile = open("UTT0001.npy", "w")
np.save(outfile, data)
outfile = open("UTT0001.npy")

print(np.load(outfile))
