import itertools
import pprint
import random
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
# import lang2vec.lang2vec as l2v

from languages import Node



"""
Compare results for various language families
"""


"""
Correlations between various languages and final scores
"""
system_scores = [
            filter_data(mean=True, system=system, aggregate=False)
            for system
            in systems
        ]

treebank_spearmans = {
    tb_code: scipy.stats.spearmanr(
        a=system_scores,
        b=[
            filter_data(mean=True, system=system, aggregate=False, tb_code=tb_code)
            for system
            in systems
        ],
    )
    for tb_code
    in treebanks
}

# for line in open('treebank_size.txt'):
#     tb_code, tb_size = line.strip().split()
#     language = tb_code_to_language(tb_code)
#     node = Node.find_by_abbrv(language)
#     if node.belongs_to(grs):
#         c = 'r'
#     else:
#         c = 'b'
#     plt.scatter(int(tb_size), treebank_spearmans[tb_code].correlation, c=c, s=3, data=tb_code)
# plt.show()


# for line in open('treebank_size.txt'):
#     tb_code, tb_size = line.strip().split()
#     language = tb_code_to_language(tb_code)
#     node = Node.find_by_abbrv(language)
#     if node.belongs_to(grs):
#         c = 'r'
#     else:
#         c = 'b'
#     plt.scatter(filter_data(mean=True, tb_code=tb_code), treebank_spearmans[tb_code].correlation, c=c, s=3, data=tb_code)
# plt.show()
# exit()


"""
Individual treebank statistics
"""

# for tb_code in treebanks:
#     y = 1 if Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs) else 0
#     plt.scatter(y, treebank_spearmans[tb_code].correlation, c='r', alpha=0.5)
#     plt.annotate(tb_code,
#                  xy=(y, treebank_spearmans[tb_code].correlation),
#                  xytext=(5, 2),
#                  textcoords='offset points',
#                  ha='right',
#                  va='bottom',
#                  fontsize='xx-small')
#
# plt.show()

# gsr_corr = [
#     corr.correlation
#     for tb_code, corr
#     in treebank_spearmans.items()
#     if Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
# ]
#
# non_gsr_corr = [
#     corr.correlation
#     for tb_code, corr
#     in treebank_spearmans.items()
#     if not Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
# ]
#
# plt.boxplot([gsr_corr, non_gsr_corr])
# plt.show()

"""
Global correlation statistics
"""

# print('Global:', np.mean([corr.correlation for corr in treebank_spearmans.values()]))
# print('GRS:', np.mean([
#     corr.correlation
#     for tb_code, corr
#     in treebank_spearmans.items()
#     if Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
# ]))
# print('Non-GRS:', np.mean([
#     corr.correlation
#     for tb_code, corr
#     in treebank_spearmans.items()
#     if not Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
# ]))

# pos, neg = [], []
# for _ in range(100):
#     random_positive = random.sample(treebanks, 49)
#     pos.append(
#         np.mean([
#             corr.correlation
#             for tb_code, corr
#             in treebank_spearmans.items()
#             if tb_code in random_positive
#         ])
#     )
#     neg.append(
#         np.mean([
#             corr.correlation
#             for tb_code, corr
#             in treebank_spearmans.items()
#             if tb_code not in random_positive
#         ])
#     )
#
# print('Random pos:', np.mean(pos), np.std(pos))
# print('Random neg:', np.mean(neg), np.std(neg))


"""
Language vectors
"""
vecs = np.load("lang_vecs.npy", allow_pickle=True, encoding='latin1')
cell_states = np.load("lang_cell_states.npy", allow_pickle=True, encoding='latin1')

print(cell_states.item().keys())
exit()
for lang in languages:
    og = lang
    if len(lang) == 2:
        try:
            lang = iso_codes[lang]
            cell_states.item()[lang][0]

            # vecs.item()['optsrc' + lang]

        except:
            print(Node.find_by_abbrv(og).name)
            print(1, lang)
    else:
        try:
            cell_states.item()[lang][0]
            # vecs.item()['optsrc'+lang]
        except:
            print(Node.find_by_abbrv(og).name)
            print(2, lang)