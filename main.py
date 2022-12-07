import os

from lang2vec import data as lang2vec_data
import lang2vec.lang2vec as l2v
import matplotlib
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import pycountry
import umap

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
        
        print('loading URIEl')
        if self.uriel:
            self.df = self.load_uriel_df()

        print('loading geo')
        if self.geo:
            df = self.load_geo_df()
            if self.df is None:
                self.df = df
            else:
                self.df = self.df.join(df, how='left')
                
        assert self.df is not None

        print('loading family')
        if self.family:
            df = self.load_family_df()
            self.df = self.df.join(df, how='left')
            
        print('loading names')
            
        self.load_language_names()
        
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
        lan_csv = pd.read_csv('./wals/wals-2020.3/raw/language.csv').set_index('pk')        # Contains geographical coordinates
        wal_csv = pd.read_csv('./wals/wals-2020.3/raw/walslanguage.csv').set_index('pk')    # Contains ISO codes    
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
        
        # df['family_str'] = [
        #     # [2:] because the families are coded with `F_` prefix
        #     # `row` is a binary vector
        #     ' '.join(family[2:] for value, family in zip(row, families_codes) if value)
        #     for row in fam_df.values
        # ]
        
        self.fields['family'] = family_codes + ['family_str']

        return df
    
    def load_language_names(self):
        pycountry.languages._load()

        self.df['name'] = [
            pycountry.languages.get(alpha_3=lang).name if lang in pycountry.languages.indices['alpha_3'] else None
            for lang in self.df.index  
        ]

        
class Visualization:
    
    def __init__(self, feature, size, zoom, backend, ldb):
        self.feature = feature
        self.size = size  # tuple
        self.zoom = zoom  # left right bottom up lims
        self.backend = backend
        self.ldb = ldb

        
    def load(self):
        # ldb = LinguisticDatabase().load()
        
        plt.clf()
        plt.rcParams["figure.figsize"] = self.size
        
        if self.feature == 'uriel':
            if self.zoom is not None:
                plt.xlim(zoom[0], zoom[1])
                plt.ylim(zoom[2], zoom[3])
                
        if self.feature == 'geo':
                
            zoom = self.zoom or (-180, 180, -60, 75)

            self.m = Basemap(
                projection='merc',
                llcrnrlat=zoom[2],
                urcrnrlat=zoom[3],
                llcrnrlon=zoom[0],
                urcrnrlon=zoom[1],
                lat_ts=20,
                resolution='c'
            )
            self.m.drawcoastlines()
            self.m.fillcontinents(color='white', lake_color='white')
            self.m.drawparallels(np.arange(-90.,91.,30.), labels=[True,False,False,False])
            self.m.drawmeridians(np.arange(-180.,181.,60.), labels=[False,True,True,False])
            self.m.drawmapboundary(fill_color='white')

        return self
    
    
    def visualize_points(self, languages=None, **kwargs):
        """
        Visualize the results for given langauges. `**kwargs` are redirected to `matplotlib.plot` and can be used to format the output.
        """
        
        if self.feature == 'uriel': 
            x = self.ldb.df.loc[languages]['uriel_x']
            y = self.ldb.df.loc[languages]['uriel_y']
            
        if self.feature == 'geo':
            lon = self.ldb.df.loc[languages]['longitude']
            lat = self.ldb.df.loc[languages]['latitude']
            x, y = self.m(lon, lat)

        plt.scatter(x, y, **kwargs)

        plt.legend()

    def show_all_languages(self, color_families=False, label_families=False, **kwargs):
        
        if not color_families:
            self.visualize_points(self.ldb.df.index, **kwargs)
            
        elif color_families:
            
            # Set default families to color - this is an arbitrary selection of some of them
            if color_families is True:
                color_families = [
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
                
            for fam in color_families:
                plt.scatter()

            # plt.scatter all the other languages as well
        
    
        
        
    