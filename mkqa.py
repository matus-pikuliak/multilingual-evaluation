import numpy as np
import matplotlib.pyplot as plt
import itertools

from language_utils.utils import fam
from languages import Node

data = dict()
for line in open('mkqa.txt'):
    lang, *scores = line.strip().split()
    scores = [float(s) for s in scores]
    data[lang] = scores

colors = itertools.cycle(['r', 'b'])

for i in range(len(scores)):
    total = np.sum([
        score[i]
        for score
        in data.values()
    ])
    non_grs = np.sum([
        score[i]
        for lang, score
        in data.items()
        if not Node.find_by_abbrv(lang[:2]).belongs_to(fam.grs)
    ])
    plt.scatter(total, non_grs, c=next(colors), s=2)

plt.show()
