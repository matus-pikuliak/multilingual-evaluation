import numpy as np
import lang2vec.lang2vec as l2v


class Uriel:
    
    coi = [
        'Atlantic-Congo',
        'Austronesian',
        'Indo-European',
        'Slavic',
        'Germanic',
        'Italic',
        'Afro-Asiatic',
        'Semitic',
        'Sino-Tibetan',
        'Nuclear_Trans_New_Guinea',
        'Pama-Nyungan',
        'Otomanguean',
        'Austroasiatic',
        'Dravidian',
        'Turkic',
        'Uralic',
    ]

    def __init__(self, load=False, *args, **kwargs):
        if load:
            self.load(*args, **kwargs)

    def load(self, languages=None, family=True, knn=True):

        if not languages:
            languages = list(l2v.available_uriel_languages())
        self.languages = languages
        if family:
            self.load_family(languages)
        if knn:
            self.load_knn(languages)

    def load_family(self, languages):
        families = [
            family[2:]
            for family
            in l2v.get_named_set(list(), 'fam')[0]  # This is the fastest way how to get the list of families.
        ]
        self.lang_fams = {
            lang: set(
                fam
                for val, fam
                in zip(vec, families)
                if val
            )
            for lang, vec
            in l2v.get_features(languages, 'fam').items()
        }

    def load_knn(self, languages):
        self.knn_matrix = np.vstack([
            vec
            for vec
            in l2v.get_features(
                languages=languages,
                feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
            ).values()
        ])

    def is_in_family(self, language, families):
#         language = l2v.LETTER_CODES.get(language, language)
        if isinstance(families, str):    
            try:
                return families in self.lang_fams[language]
            except AttributeError:
                raise AttributeError('You should load with family=true')
        else:
            return any(self.is_in_family(language, fam) for fam in families)