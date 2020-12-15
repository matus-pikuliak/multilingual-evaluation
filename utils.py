from types import SimpleNamespace

from languages import Node


def tb_code_to_language(tb_code):
    if '_' in tb_code:
        language, _ = tb_code.split('_')
        language = {
            'bxr': 'bua',
            'kmr': 'ku',
            'sme': 'se',
        }.get(language, language)
        return language
    else:
        return None


def tb_code_belongs_to(tb_code, family):
    language = tb_code_to_language(tb_code)
    return Node.find_by_abbrv(language).belongs_to(family)


fam = SimpleNamespace(
    indo={'Indo-European'},
    grs={'Germanic', 'Italic', 'Slavic'},
)

tb_sizes = {}
for line in open('language_utils/treebank_size.txt'):
    tb_code, tb_size = line.strip().split()
    tb_sizes[tb_code] = int(tb_size)



