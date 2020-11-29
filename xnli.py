import numpy as np
import matplotlib.pyplot as plt

from language_utils.utils import fam
from languages import Node

langs = 'en fr es de el bg ru tr ar vi th zh hi sw ur'.split()

for line in open('xnli.txt'):
    scores = line.strip().split()
    scores = [float(s) for s in scores]

    total = np.mean(scores)
    non_grs = np.mean([
        s
        for i, s
        in enumerate(scores)
        if not Node.find_by_abbrv(langs[i]).belongs_to(fam.indo)
    ])
    plt.scatter(total, non_grs, c='r', s=2)

plt.show()
