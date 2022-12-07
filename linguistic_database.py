import os

from lang2vec import data as lang2vec_data
import lang2vec.lang2vec as l2v
import numpy as np
import pandas as pd
import pycountry
import umap


from utils import create_logger
logger = create_logger('ldb')


class LinguisticDatabase:
    
    def __init__(
        self,
        uriel=True,
        uriel_umap=True,
        family=True,
        geo=True,
    ):
        self.uriel = uriel
        self.uriel_umap = uriel_umap
        self.family = family
        self.geo = geo
        self.df = None
        self.fields = dict()
        
    def load(self):
        
        logger.info('Loading Linguistic Database. This might take a minute.')
        logger.info('Loading URIEL features.')
        if self.uriel:
            self.df = self.load_uriel_df()

        logger.info('Loading geographical features.')
        if self.geo:
            df = self.load_geo_df()
            if self.df is None:
                self.df = df
            else:
                self.df = self.df.join(df, how='left')
                
        assert self.df is not None

        logger.info('Loading family features.')
        if self.family:
            df = self.load_family_df()
            self.df = self.df.join(df, how='left')
            
        logger.info('Loading language names.')
        self.load_language_names()
        
        logger.info('Loading done.')
        
        return self
            
            
    def load_uriel_df(self):
        # `available_uriel_languages` from lang2vec is bugged so we need to extract languages manually
        dt = np.load(os.path.join(lang2vec_data.__path__[0], 'feature_predictions.npz'))

        uriel_languages = sorted(dt['langs'])

        uriel_features = l2v.get_features(
            languages=uriel_languages,
            feature_set_inp='syntax_knn+phonology_knn+inventory_knn',
            header=True,
        )

        # CODE is a special value for feature names
        uriel_codes = uriel_features['CODE']
        self.fields['uriel'] = uriel_codes

        df = pd.DataFrame(
            [uriel_features[lang] for lang in uriel_languages],
            index=uriel_languages,
            columns=uriel_codes,
        )
        
        if self.uriel_umap:
            
            self.uriel_umap_object = umap.UMAP(
                n_neighbors=200,
                metric='cosine',
                min_dist=0.5,
                random_state=1,
            )
            self.uriel_umap_object.fit(df[uriel_codes].values)

            df['uriel_x'] = self.uriel_umap_object.embedding_[:,0]
            df['uriel_y'] = self.uriel_umap_object.embedding_[:,1]
            self.fields['uriel_umap'] = ['uriel_x', 'uriel_y']

        return df
    
    def load_geo_df(self):
        

        # WALS files downloaded from https://github.com/cldf-datasets/wals/releases
        lan_csv = pd.read_csv('./wals-2020.3/raw/language.csv').set_index('pk')        # Contains geographical coordinates
        wal_csv = pd.read_csv('./wals-2020.3/raw/walslanguage.csv').set_index('pk')    # Contains ISO codes    
        df = lan_csv.join(wal_csv)

        # Normalize ISO codes, some are null, some have multiple variants (we take first)
        df = df[df.iso_codes.notna()]
        df['iso_codes'] = df['iso_codes'].apply(lambda s: s.split(', ')[0])

        df = df[['iso_codes', 'latitude', 'longitude']].set_index('iso_codes')
        self.fields['geo'] = ['latitude', 'longitude']

        # Multiple records can share one ISO code (e.g. Zulu, Zulu (northern), Zulu (southerns)) and they can even have different primary key
        # in `languages.csv` and different geographical coordinates. Here we simply select the first record. This might not be an optimal
        # solution, but it is only a handful of languages and I believe that the coordinates will still roughly match.
        df = df[~df.index.duplicated()]
        
        return df

    
    def load_family_df(self):
        families = l2v.get_features(
            languages=list(self.df.index),
            feature_set_inp='fam',
            header=True,
        )
        
        family_codes = families['CODE']
        
        df = pd.DataFrame(
            [families[lang] for lang in self.df.index],
            index=self.df.index,
            columns=family_codes,
        )
        
        self.fields['family'] = family_codes + ['family_str']

        return df
    
    def load_language_names(self):
        pycountry.languages._load()

        self.df['name'] = [
            pycountry.languages.get(alpha_3=lang).name if lang in pycountry.languages.indices['alpha_3'] else None
            for lang in self.df.index  
        ]