import numpy as np


class Uriel:

    def __init__(self, load=False, *args, **kwargs):
        import lang2vec.lang2vec as l2v
        self.l2v = l2v
        if load:
            self.load(*args, **kwargs)

    def load(self, languages=None, family=True, knn=True):

        if not languages:
            languages = list(self.l2v.available_uriel_languages())
        self.languages = languages
        if family:
            self.load_family(languages)
        if knn:
            self.load_knn(languages)

    def load_family(self, languages):
        families = [
            family[2:]
            for family
            in self.l2v.get_named_set(list(), 'fam')[0]  # This is the fastest way how to get the list of families.
        ]
        self.lang_fams = {
            lang: set(
                fam
                for val, fam
                in zip(vec, families)
                if val
            )
            for lang, vec
            in self.l2v.get_features(languages, 'fam').items()
        }

    def load_knn(self, languages):
        self.knn_matrix = np.vstack([
            vec
            for vec
            in self.l2v.get_features(
                languages=languages,
                feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
            ).values()
        ])

    def is_in_family(self, language, family):
        try:
            return family in self.lang_fams[language]
        except AttributeError:
            raise AttributeError('You should load with family=true')

# u = Uriel()
# u.load(['en', 'sk'], family=False)
# print(u.is_in_family('en', 'Baltic'))