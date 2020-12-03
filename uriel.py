import lang2vec.lang2vec as l2v
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt

from language_utils.utils import fam
from languages import Node, Language


# families = list(np.load('family_features.npz')['feats'])
# vecs = l2v.get_features(list(l2v.LANGUAGES), 'fam')
# counter = {i: 0 for i in range(3718)}
# for l, v in vecs.items():
#     print(l)
#     for i, e in enumerate(v):
#         if e:
#             counter[i] += 1
# print(counter)

# exit()
#
#
langs = list(l2v.LEARNED_LETTER_CODES.difference({'alb', 'sqi'}))
# final = list(set(my_codes).intersection(set(langs)))
final = l2v.available_uriel_languages()

data = np.vstack([
    vec
    for vec
    in l2v.get_features(
        languages=list(l2v.available_uriel_languages())[:100],
        feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
    ).values()
])


reducer = umap.UMAP(n_neighbors=200, metric='cosine')
trans = reducer.fit(data)
umap.plot.points(
    trans,
    labels=np.array([0 for _ in range(data.shape[0])])
)
