import numpy as np
from types import FunctionType
from utils import language_iso

from ud_parser.ud_parser import UDScores

def rahimi_ner():
    languages = [line.split()[0] for line in open('./papers/rahimi_ner.txt')]
    scores = np.vstack([
        [float(v) for v in line.split()[2:]]
        for line
        in open('./papers/rahimi_ner.txt')
    ])
    return languages, scores

def heinzerling_ner():
    languages = [line.split()[0] for line in open('./papers/heinzerling_ner.txt')]
    scores = np.vstack([
        [float(v) for v in line.split()[1:]]
        for line
        in open('./papers/heinzerling_ner.txt')
    ])
    return languages, scores

def heinzerling_pos():
    languages = [line.split()[0] for line in open('./papers/heinzerling_pos.txt')]
    scores = np.vstack([
        [float(v) for v in line.split()[1:]]
        for line
        in open('./papers/heinzerling_pos.txt')
    ])
    return languages, scores

def artetxe_nli():
    languages = 'en fr es de el bg ru tr ar vi th zh hi sw ur'.split()
    scores = np.vstack([
        list(map(float, line.split()))
        for line
        in open('./papers/artetxe_nli.txt')
    ]).T
    return languages, scores

def artetxe_nli_2():
    languages = 'en fr es de el bg ru tr ar vi th zh hi sw ur'.split()
    scores = np.vstack([
        list(map(float, line.split()))
        for line
        in open('./papers/artetxe_nli_2.txt')
    ]).T
    return languages, scores

def huang_nli():
    languages = 'en fr es de el bg ru tr ar vi th zh hi sw ur'.split()
    scores = np.vstack([
        list(map(float, line.split()))
        for line
        in open('./papers/huang_nli.txt')
    ]).T
    return languages, scores

def longpre_qa_em():
    languages = [line[:2] for line in open('./papers/longpre_qa.txt')]
    scores = np.vstack([
        list(map(float, line.split()[1:]))
        for line
        in open('./papers/longpre_qa.txt')
    ])
    return languages, scores[:, 0::2]

def longpre_qa_f1():
    languages = [line[:2] for line in open('./papers/longpre_qa.txt')]
    scores = np.vstack([
        list(map(float, line.split()[1:]))
        for line
        in open('./papers/longpre_qa.txt')
    ])
    return languages, scores[:, 1::2]

def wang_ner():
    languages = [line.split()[0] for line in open('./papers/wang_ner.txt')]
    scores = np.vstack([
        [float(v) for v in line.split()[1:]]
        for line
        in open('./papers/wang_ner.txt')
    ])
    return languages, scores

def ud(metric='las'):
    parser = UDScores(metric=metric)
    data = parser.get_data()
    data = [datum for datum in data if datum.system != 'SParse (İstanbul)']
    treebanks = set(d.tb_code for d in data if not d.aggregate)
    languages = [next(d for d in data if d.tb_code == tb).language for tb in treebanks]
    systems = list(set(d.system for d in data))
    scores = np.vstack([
        np.array([
            next(d.perf for d in data if d.system == s and d.tb_code == t)
            for s
            in systems
        ])
        for t
        in treebanks
    ])
    return languages, scores

papers = {
    s: language_iso(f)()
    for s, f
    in dict(locals()).items()
    if isinstance(f, FunctionType) and f is not language_iso
}