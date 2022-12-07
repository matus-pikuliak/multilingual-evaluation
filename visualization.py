from lang2vec import lang2vec as l2v
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.basemap import Basemap
import numpy as np


class Visualization:
    
    def __init__(self, feature, size, zoom, backend, ldb):
        """
        Initialize `Visualization` object.
        
        `feature` can be _uriel_ or _geo_
        `size` is a width, height tuple
        `zoom` defines the parts of the map that is visualized in left right bottom up order 
        `backend` can be _matplotlib_ or _bokeh_
        `ldb` is a initialized and loaded _LinguisticDatabase_ object
        """
        self.feature = feature
        self.size = size
        self.zoom = zoom
        self.backend = backend
        self.ldb = ldb

        
    def load(self):
        """
        Prepare the canvas for further visualizations.
        """
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
  

    def finish(self):
        """
        Finish the visualizations
        """
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
    
    def visualize_points(self, languages=None, **kwargs):
        """
        Visualize `langauges` on the map.
        
        `languages` are a list of ISO-639 codes. 639-3 is recommended.
        `**kwargs` are redirected to `matplotlib.plot` and can be used to format the output.
        """
        languages = [l2v.LETTER_CODES.get(l, l) for l in languages]
        
        if self.feature == 'uriel': 
            x = self.ldb.df.loc[languages]['uriel_x']
            y = self.ldb.df.loc[languages]['uriel_y']
            
        if self.feature == 'geo':
            lon = self.ldb.df.loc[languages]['longitude']
            lat = self.ldb.df.loc[languages]['latitude']
            x, y = self.m(lon, lat)

        # zorder is there mainly for geographical projection
        plt.scatter(x, y, zorder=3, **kwargs)

        
    def show_all_languages(self, color_families=False, label_families=False, **kwargs):
        """
        Visualize all the languages in our database on the map.
        
        `color_families` can be used to colorize certain language families. If True is used, our default list is used.
          Otherwise you can define your own list.
        `label_families` whether to list the colorized families in the legend
        `**kwargs` are redirected to `matplotlib.plot` and can be used to format the output.
        """
        
        if not color_families:
            self.visualize_points(self.ldb.df.index, **kwargs)
            
        elif color_families:
            
            # Set default families to color - this is an arbitrary selection of some of them
            if color_families is True:
                color_families = [
                    'Atlantic-Congo',
                    'Austronesian',
                    'Slavic',
                    'Germanic',
                    'Italic',
                    'Indo-European',
                    'Semitic',
                    'Afro-Asiatic',
                    'Dravidian',
                    'Turkic',
                    'Uralic',
                    'Nuclear_Trans_New_Guinea',
                    'Sino-Tibetan',
                    'Pama-Nyungan',
                    'Austroasiatic',
                    'Otomanguean',
                ]
                
            # each row is a binary family vector for a language
            fam_vectors = self.ldb.df[[f'F_{fam}' for fam in color_families]].values
            
            # id of the first matching family for each language. this way we use subsets in the definition, if the subset is defined first, e.g. Germanic and Indo-European in the list above
            fam_ids = np.array([next((i for i, v in enumerate(row) if v), -1) for row in fam_vectors])  
            
            # visualize indiviudal languages
            for i in range(len(color_families)):
                languages = self.ldb.df.index[np.squeeze(np.argwhere(fam_ids==i))]
                self.visualize_points(languages, c=list(mcolors.TABLEAU_COLORS)[i % 10], **kwargs)
                
            # set up labels
            if label_families:
                for i, fam in enumerate(color_families):
                    plt.scatter([], [], c=list(mcolors.TABLEAU_COLORS)[i % 10], label=fam)
                    
            # visualize all the other languages
            other = self.ldb.df.index[np.squeeze(np.argwhere(fam_ids==-1))]
            self.visualize_points(other, c='gray', **kwargs)
    
    
    def show_languages(self, languages, c='r', s=50, alpha=0.5):
        """
        Simply show all the `languages` on the map
        """
        self.visualize_points(languages, c=c, s=s, alpha=alpha)

        
    
        
        
    