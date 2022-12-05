import lang2vec.lang2vec as l2v
import numpy as np
import pandas as pd
import umap

from utils import isos

class Uriel:
    
    def __init__(self):
        uriel_languages = sorted(l2v.available_uriel_languages())
        
        uriel_features = l2v.get_features(
            languages=uriel_languages,
            feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
            header=True,
        )
        
        df = pd.DataFrame(
            [uriel_features[l] for l in uriel_languages],
            index=uriel_languages,
            columns=uriel_features['CODE']
        )
        
        
        
        # load URIEL features
        # calculate UMAP x, y coordinates
        # load family features
        # load geo-features
        
  
    def load(self, family=True, knn=True, umap=False):
        self.uriel_languages = list()
        self.fam_languages = list(sorted(l2v.available_languages()))
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
            random_state=2,
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
            in .values()
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
