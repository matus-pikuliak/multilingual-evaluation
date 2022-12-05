from types import SimpleNamespace
from lang2vec.lang2vec import LETTER_CODES

isos = dict(
    line.strip().split(maxsplit=1)
    for line
    in open('iso.txt')
)


# Some macro-languages are not represented in the URIEL database, e.g. there is no record for Arabic, only individual dialects. Here we switch from
# several common macrolangauges to individual languages by using our best heuristic. E.g. for Cree we selected Plains Cree dialect because it is the
# most common
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

def normalize_to_iso(lang):
    lang = LETTER_CODES.get(lang, lang)  # LETTER_CODES from lang2vec library. They include ISO-693 switch from 2 to 3 letters
    lang = ISO_SWITCH.get(lang, lang)  # Some left-over problems we were able to identify
    raise if not in uriel_languages...
    return lang
    



