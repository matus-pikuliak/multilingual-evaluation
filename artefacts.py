import numpy as np
import matplotlib.pyplot as plt

langs = 'en fr es de el bg ru tr ar vi th zh hi sw ur'.split()
mask = [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

data = [
    list(map(float, line.split()))
    for line
    in open('artefacts.txt')
]

for i, m in enumerate(data):
    total = np.mean(m)
    non_grs = np.mean([a for a, b in zip(m, mask) if b])
    plt.scatter(total, non_grs, s=2, c='r')
    plt.annotate(i,
                 xy=(total, non_grs),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom',
                 fontsize='xx-small')
plt.plot([0, 100], [0, 100])
plt.show()