import wordtree
import pandas as pd
import networkx as nx
import pydotplus
import re
import json


class FreqNode():
    def __init__(self, kw, children, freq):
        self.name = kw
        self.children = children
        self.freq = freq

    def __str__(self):
        print(self.name)
        for c in self.children:
            print(" " + str(c))


def build_tree(kw, ngrams, frequencies):
    tree = FreqNode(kw, {}, 0)
    for ngram, freq in zip(ngrams, frequencies):
        subtree = tree
        for gram in ngram:
            if gram not in subtree.children:
                subtree.children[gram] = FreqNode(gram, {}, freq)
            subtree = subtree.children[gram]
        subtree.freq = freq
    return tree


def build_both_trees(keyword, ngrams, frequencies):
    fwd_ngrams, fwd_frequencies = [], []
    bwd_ngrams, bwd_frequencies = [], []

    for ngram, freq in zip(ngrams, frequencies):
        fwd = ngram[0] == keyword
        bwd = ngram[-1] == keyword
        assert fwd or bwd, "ngram does not have keyword at beginning or end: {}".format(
            ngram)

        if fwd:
            fwd_ngrams.append(ngram[1:])
            fwd_frequencies.append(freq)
        if bwd:
            bwd_ngrams.append(reversed(ngram[:-1]))
            bwd_frequencies.append(freq)

    fwd_tree = build_tree(keyword, fwd_ngrams, fwd_frequencies)
    # bwd_tree = build_tree(keyword, bwd_ngrams, bwd_frequencies)

    return fwd_tree  # , bwd_tree


def visit(out, edges):

    if out["name"] not in edges:
        return out

    for ch in edges[out['name']]:
        out['children'].append(visit({'name': ch, "children": []}, edges))
    return out


def generate_json(filename, keyword):
    ds = pd.read_csv(filename)
    ds = ds["Summary"].dropna().to_list()

    g = wordtree.search_and_draw(corpus=ds, keyword=keyword)
    dotplus = pydotplus.graph_from_dot_data(g.source)
    nx_graph = nx.nx_pydot.from_pydot(dotplus)

    edges = list(nx_graph.out_edges)

    edges = list(map(lambda x: (
        x[0], x[1]), edges))

    d = dict()

    for a, b in edges:
        if a not in d:
            d[a] = []
        d[a].append(b)

    out = visit({'name': keyword, "children": []}, d)

    st = json.dumps(out)

    tokens = re.findall(".*?\"name\": \"(.*?)\".*?", st)

    for t in tokens:
        st = st.replace(t, t.split("-")[-1])
    return json.loads(st)
