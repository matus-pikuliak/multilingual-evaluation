import itertools
import pprint
import random
import re
from collections import defaultdict
from html.parser import HTMLParser
import requests
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

from languages import Node

html = requests.get('https://universaldependencies.org/conll18/results-blex.html').text


class UDParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.state = None
        self.current_title = None
        self.data = dict()

    def handle_starttag(self, tag, attrs):
        self.state = {
            'h3': 'title',
            'h2': 'title',
            'pre': 'table'
        }.get(tag, None)

    def handle_endtag(self, tag):
        self.state = None

    def handle_data(self, data):
        if self.state == 'title':
            self.current_title = data
        if self.state == 'table':
            self.data[self.current_title] = self.parse_table(data)

    @staticmethod
    def parse_table(table):
        return {
            line[5:40].rstrip(): float(line[-5:])
            for line
            in table.split('\n')
            if line
        }


parser = UDParser()
parser.feed(html)


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


data = []

for tb_code, tb_results in parser.data.items():

    for system, perf in tb_results.items():

        data.append(
            {
                'tb_code': tb_code,
                'aggregate': '_' not in tb_code,
                'language': tb_code_to_language(tb_code),
                'system': system,
                'perf': perf
            }
        )

systems = set(datum['system'] for datum in data)
languages = set(datum['language'] for datum in data).difference({None})
treebanks = set(datum['tb_code'] for datum in data if datum['language'])


def filter_data(mean=False, **kwargs):
    def filter_function(datum):
        return all(datum[key] == value for key, value in kwargs.items())
    filtered = filter(filter_function, data)
    if mean:
        return np.mean([datum['perf'] for datum in filtered])
    else:
        return filtered

indo = {'Indo-European'}
grs = {'Germanic', 'Italic', 'Slavic'}

"""
Show results for individual languages
"""
# for line in open('treebank_size.txt'):
#     tb_code, tb_size = line.strip().split()
#     perf = filter_data(mean=True, tb_code=tb_code)
#     language = tb_code_to_language(tb_code)
#     node = Node.find_by_abbrv(language)
#     if node.belongs_to(grs):
#         c = 'r'
#     else:
#         c = 'b'
#     plt.scatter(int(tb_size), perf, c=c, s=3, data=tb_code)
#     plt.annotate(tb_code,
#                  xy=(int(tb_size), perf),
#                  xytext=(5, 2),
#                  textcoords='offset points',
#                  ha='right',
#                  va='bottom',
#                  fontsize='xx-small')
# plt.show()

"""
Compare results for various language families
"""
# for system in systems:
#     mean = filter_data(mean=True, system=system, aggregate=False) / 100
#     system_data = list(filter_data(system=system, aggregate=False))
#     high_mean = np.mean([
#         datum['perf']
#         for datum
#         in system_data
#         if Node.find_by_abbrv(datum['language']).belongs_to(grs)
#     ]) / 100
#     low_mean = np.mean([
#         datum['perf']
#         for datum
#         in system_data
#         if not Node.find_by_abbrv(datum['language']).belongs_to(grs)
#     ]) / 100
#     plt.scatter(mean, high_mean, c='b', s=2)
#
# plt.plot([0, 1], [0, 1])
# plt.show()

system_scores = [
            filter_data(mean=True, system=system, aggregate=False)
            for system
            in systems
        ]

treebank_spearmans = {
    tb_code: scipy.stats.spearmanr(
        a=system_scores,
        b=[
            filter_data(mean=True, system=system, aggregate=False, tb_code=tb_code)
            for system
            in systems
        ],
    )
    for tb_code
    in treebanks
}

print('Global:', np.mean([corr.correlation for corr in treebank_spearmans.values()]))
print('GRS:', np.mean([
    corr.correlation
    for tb_code, corr
    in treebank_spearmans.items()
    if Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
]))
print('Non-GRS:', np.mean([
    corr.correlation
    for tb_code, corr
    in treebank_spearmans.items()
    if not Node.find_by_abbrv(tb_code_to_language(tb_code)).belongs_to(grs)
]))

pos, neg = [], []
for _ in range(100):
    random_positive = random.sample(treebanks, 49)
    pos.append(
        np.mean([
            corr.correlation
            for tb_code, corr
            in treebank_spearmans.items()
            if tb_code in random_positive
        ])
    )
    neg.append(
        np.mean([
            corr.correlation
            for tb_code, corr
            in treebank_spearmans.items()
            if tb_code not in random_positive
        ])
    )

print('Random pos:', np.mean(pos), np.std(pos))
print('Random neg:', np.mean(neg), np.std(neg))