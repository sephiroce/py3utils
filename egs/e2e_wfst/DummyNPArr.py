import numpy as np
"""
data=np.array([[0,2.1,0,1.1, 0],
    [0,0,1.1,2.1,0],
    [0,1.1,2.1,0,0],
    [0,0,2.1,0,0.1]])
    """
data = np.random.uniform(low=0.01, high=1.0, size=(10,10026))
# Saving data
np.save("UTT0001.npy", data)

# Loaing data
arr = np.load("UTT0001.npy")
print(arr)
print(arr.shape)
