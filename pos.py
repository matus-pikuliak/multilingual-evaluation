import numpy as np
import matplotlib.pyplot as plt
import itertools

from language_utils.utils import fam
from languages import Node

data = dict()
for line in open('pos.txt'):
    lang, *scores = line.strip().split()
    scores = [float(s) for s in scores]
    data[lang] = scores
    # try:
    #     Node.find_by_abbrv(lang)
    # except AttributeError as e:
    #     print(e)

for i in range(len(scores)):
    total = np.mean([
        score[i]
        for score
        in data.values()
    ])
    non_grs = np.mean([
        score[i]
        for lang, score
        in data.items()
        if not Node.find_by_abbrv(lang).belongs_to(fam.grs)
    ])
    plt.scatter(total, non_grs, c='r', s=2)
    plt.annotate(i,
                 xy=(total, non_grs),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom',
                 fontsize='xx-small')

plt.plot([0, 100], [0, 100])
plt.show()
