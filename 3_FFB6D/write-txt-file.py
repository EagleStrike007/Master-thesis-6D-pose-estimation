import numpy as np

"""
Making a .txt file
"""
lines = np.arange(200, 500, 1)

with open('train.txt', 'w') as f:
    for line in lines:
        f.write("%06d" % line)
        f.write('\n')
