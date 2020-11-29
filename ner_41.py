import numpy as np
import matplotlib.pyplot as plt

from languages import Node
from language_utils.utils import fam

recs = {}
for line in open('ner_42.txt'):
    language, *scores = line.strip().split()
    scores = [int(score) for score in scores]
    recs[language] = scores
    print(Node.find_by_abbrv(language).name, Node.find_by_abbrv(language).parents())

print('Total:', len(recs))
print('Indo-E:', sum(
    Node.find_by_abbrv(lang).belongs_to(fam.indo)
    for lang
    in recs
))
print('GRS:', sum(
    Node.find_by_abbrv(lang).belongs_to(fam.grs)
    for lang
    in recs
))
for l in fam.grs:
    print(f'{l}:', sum(
    Node.find_by_abbrv(lang).belongs_to({l})
    for lang
    in recs
))
print()


def weight(lang):
    if Node.find_by_abbrv(lang).belongs_to(fam.grs):
        return 1
    else:
        return 7


for i in range(len(scores)):
    total_avg = np.mean([
        score[i] * weight(lang)
        for lang, score
        in recs.items()
    ])
    indo_avg = np.mean([
        score[i]
        for lang, score
        in recs.items()
        if not Node.find_by_abbrv(lang).belongs_to(fam.grs)
    ])
    plt.scatter(total_avg, indo_avg, c='r', s=2)
    plt.annotate(i,
                 xy=(total_avg, indo_avg),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom',
                 fontsize='xx-small')

plt.plot([0, 100], [0, 100])
plt.show()