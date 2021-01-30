import lang2vec.lang2vec as l2v
import numpy as np
import pandas as pd
import umap

from utils import isos

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
        elif args or kwargs:
            raise AttributeError('Arguments lost without load=True.')

            
    def load(self, family=True, knn=True, umap=False):
        self.uriel_languages = list(l2v.available_uriel_languages())
        self.fam_languages = list(l2v.available_languages())
        if family:
            self.lang_fams = self.load_family(self.fam_languages)
        if knn:
            self.knn_matrix = self.load_knn(self.uriel_languages)
        if umap:
            self.umap_vectors = self.load_umap(self.knn_matrix)
        
        
    @staticmethod
    def load_umap(knn_matrix):
        umap_object = umap.UMAP(
            n_neighbors=15,
            metric='cosine',
            min_dist=0.5,
            random_state=1,
        )
        return umap_object.fit(knn_matrix)

    
    @staticmethod
    def load_family(languages):
        families = [
            family[2:]
            for family
            in l2v.get_named_set(list(), 'fam')[0]  # This is the fastest way how to get the list of families.
        ]
        return {
            lang: set(
                fam
                for val, fam
                in zip(vec, families)
                if val
            )
            for lang, vec
            in l2v.get_features(languages, 'fam').items()
        }

    
    @staticmethod
    def load_knn(languages):
        return np.vstack([
            vec
            for vec
            in l2v.get_features(
                languages=languages,
                feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
            ).values()
        ])
    
    
    def language_metadata(self, languages):
        return pd.DataFrame({
            'fam': [' '.join(self.lang_fams[l]) for l in languages],
            'code': languages,
            'lang': [isos.get(lang, lang) for lang in languages],
            'label': [
                max(
                    [0] + [
                        i + 1
                        for i, c
                        in enumerate(self.coi)
                        if c in self.lang_fams[lang]
                    ]
                )
                for lang
                in languages
            ]
        })
    
    
    def is_in_family(self, language, families):
        if isinstance(families, str):    
            try:
                return families in self.lang_fams[language]
            except AttributeError:
                raise AttributeError('You should load with family=true')
            except KeyError:
                return False
        else:
            return any(self.is_in_family(language, fam) for fam in families)
     
    
    def weights(self, languages, temperature=10, distance='cos', measure='mea'):

        def cos(l1, l2):
            return 1 - sum(l1/np.linalg.norm(l1) * (l2/np.linalg.norm(l2)))
        def euc(l1, l2):
            return np.sqrt(sum((l1 - l2)**2))
        def jac(l1, l2):
            return 1 - sum(l1 & l2) / sum(l1 | l1)

        vectors = self.knn_matrix[[self.uriel_languages.index(l) for l in languages]].astype(int)
        similarities = np.array([
            {'mea': np.mean, 'med': np.median}[measure]([
                {'euc': euc, 'jac': jac, 'cos': cos}[distance](vectors[i1], vectors[i2])
                for i1
                in range(len(vectors))
                if i1 != i2
            ])
            for i2 in range(len(vectors))
        ])
        weights = (np.e ** temperature) ** similarities
        weights /= np.sum(weights)

        return {
            lang: score
            for lang, score
            in zip(languages, weights)
        }
