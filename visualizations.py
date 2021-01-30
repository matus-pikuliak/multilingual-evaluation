from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import umap
import umap.plot
import bokeh.plotting
import pandas as pd
import numpy as np

from utils import isos

def show_uriel(u):
    metadata = u.language_metadata(u.uriel_languages)
    p = umap.plot.interactive(
        u.umap_vectors,
        labels=metadata['label'],
        hover_data=metadata,
        width=600,
        height=600,
        interactive_text_search=True,
        point_size=4,
        interactive_text_search_alpha_contrast=0.99,
        theme='blue',
    )
    bokeh.plotting.output_notebook() 
    bokeh.plotting.show(p)
    
def show_uriel_connectivity(u):
    umap.plot.connectivity(u.umap_vectors, show_points=True, edge_bundling='hammer')

def show_languages(u, languages):
    metadata = u.language_metadata(u.uriel_languages)
    p = umap.plot.interactive(
        u.umap_vectors,
        hover_data=metadata,
        width=600,
        height=600,
        interactive_text_search=True,
        point_size=2,
        interactive_text_search_alpha_contrast=0.99,
    )
    metadata = metadata[metadata['code'].isin(languages)]
    for l in set(languages) - set(metadata['code']):
        print(f'Language {isos[l]} ({l}) not supported. It will be removed from visualization')
    metadata = metadata.assign(
        x=u.umap_vectors.embedding_[metadata.index][:,0],
        y=u.umap_vectors.embedding_[metadata.index][:,1],
    )
    p.children[1].circle(
        x='x',
        y='y',
        size=10,
        alpha=0.5,
        color="#ee6666",
        source=metadata
    )

    bokeh.plotting.output_notebook() 
    bokeh.plotting.show(p)
    
def show_diff(u, languages, score1, score2, comparison='rel'):
    score1 = dict(zip(languages, score1))
    score2 = dict(zip(languages, score2))
    metadata = u.language_metadata(u.uriel_languages)
    p = umap.plot.interactive(
        u.umap_vectors,
        hover_data=metadata,
        width=600,
        height=600,
        interactive_text_search=True,
        point_size=2,
        interactive_text_search_alpha_contrast=0.99,
        cmap=LinearSegmentedColormap.from_list('oink', ['#eee', '#ccc']),
    )
    metadata = metadata[metadata['code'].isin(languages)]
    if comparison == 'rel':
        diff = {l: score2[l] / score1[l] - 1 for l in metadata['code']}
    if comparison == 'abs':
        diff = {l: score2[l] - score1[l] for l in metadata['code']}
    metadata = metadata.assign(
        x=u.umap_vectors.embedding_[metadata.index][:,0],
        y=u.umap_vectors.embedding_[metadata.index][:,1],
        width=0.05,
        height=[abs(diff[l]) for l in metadata['code']],
        color=['#66ee66' if diff[l] > 0 else '#ee6666' for l in metadata['code']],
    )
    metadata['height'] /= max(metadata['height'])
    metadata['height'] *= 2
    metadata['y'] += metadata['height'] / 2
    p.children[1].rect(
        x='x',
        y='y',
        width='width',
        height='height',
        color='color',
        source=metadata,
    )

    bokeh.plotting.output_notebook() 
    bokeh.plotting.show(p)

def show_weights(u, weights):
    max_ = max(weights.values())
    metadata = u.language_metadata(u.uriel_languages)
    p = umap.plot.interactive(
        u.umap_vectors,
        hover_data=metadata,
        width=600,
        height=600,
        interactive_text_search=True,
        point_size=2,
        interactive_text_search_alpha_contrast=0.99,
    )
    metadata = metadata[metadata['code'].isin(weights)]
    metadata = metadata.assign(
        x=u.umap_vectors.embedding_[metadata.index][:,0],
        y=u.umap_vectors.embedding_[metadata.index][:,1],
        width=0.05,
        height=[weights[l]*5/max_ for l in metadata['code']],
        alpha=1,
    )
    metadata['y'] += metadata['height'] / 2
    p.children[1].rect(
        x='x',
        y='y',
        width='width',
        height='height',
        color="#ee6666",
        source=metadata,
    )

    bokeh.plotting.output_notebook() 
    bokeh.plotting.show(p)
    
def show_families(u, languages):
    d = pd.DataFrame(
        [
            (
                fam,
                (count := sum(u.is_in_family(language, fam) for language in languages)),
                100 * count / len(languages)
            )
             for fam
             in u.coi
        ],
        columns=['Family', 'Count', 'Ratio']
    )
    print(d)
    
def show_methods(u, languages, scores, family):
    xs = np.mean(scores, axis=0)        
    ys_in = np.mean(scores[
            [i
             for i, l
             in enumerate(languages)
             if u.is_in_family(l, family)
            ]
        ], axis=0)
    ys_out = np.mean(scores[
        [i
         for i, l
         in enumerate(languages)
         if not u.is_in_family(l, family)
        ]
    ], axis=0)
    fig, axes = plt.subplots(1, 2)
    for ax, ys, ylabel in zip(axes, [ys_in, ys_out], [f'Languages in {" ".join(family)}', f'Languages not in {" ".join(family)}']):
        col = LineCollection(segments=[[(0,0), (100,100)]], linewidths=1, colors='b')
        ax.add_collection(col, autolim=False)
        ax.scatter(xs, ys, c='r', s=2)
        ax.set_xlabel('Total average')
        ax.set_ylabel(ylabel)
        for i, xy in enumerate(zip(xs, ys)):     
            ax.annotate(
                text=i,
                xy=xy,
                xytext=(1, 1),
                textcoords='offset points',
                ha='right',
                va='bottom',
                fontsize='xx-small')
    fig.show()
