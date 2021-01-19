from types import SimpleNamespace
from lang2vec.lang2vec import LETTER_CODES

fam = SimpleNamespace(
    indo={'Indo-European'},
    gis={'Germanic', 'Italic', 'Slavic'},
)

isos = dict(
    line.strip().split(maxsplit=1)
    for line
    in open('iso.txt')
)

ISO_SWITCH = {
    'sqi': 'alb',  # l2v bug
    'zho': 'cmn',  # Mandarin Chinese
    'fas': 'pes',  # Iranian persian
    'ara': 'arb',  # Standard Arabic
    'swa': 'swh',  # Coastal Swahili (?)
    'msa': 'zlm',  # Malay (individual language)
    'uzb': 'uzn',  # Northern Uzbek (?)
    'orm': 'gaz',  # West Central Oromo (?)
    'kon': 'kng',  # Koongo
    'vls': 'zea',  # vls is alternative code
    'grn': 'gug',  # Guarani is official language of Paraguay and gug is Paraguayi variant
    'aze': 'azj',  # Northern Azerbaijani in Latin script
    'ful': 'fuf',  # Fula centroid in UMAP
    'mon': 'khk',  # Khalkha Mongolian
    'srd': 'sro',  # Campidanese Sardinian (only available)  
    'nno': 'nor',  # Norwegian
    'cre': 'crl',  # Plains Cree
    'ipk': 'esi',  # North Alaskan Inupiatun (only available)
    'pus': 'pst',  # Central Pashto (only available)
    'kom': 'kpv',  # kom is alternative code
    'hbs': 'srp',  # Serbian
    'que': 'qvs',  # San Martin Quechuan (centroid)
    'zha': 'zgb',  # Guibei Zhuang(only available)
    'iku': 'ike',  # Eastern Canadian Inuktitut
}

def language_iso(func):
    
    def wrap():
        ls, s = func()
        ls = [LETTER_CODES.get(l, l) for l in ls]
        ls = [ISO_SWITCH.get(l, l) for l in ls]
        return ls, s
    
    return wrap

