import wordtree
import pandas as pd
import networkx as nx
import pydotplus
from nltk.tokenize import word_tokenize
import re
import json

from string import punctuation, digits


def visit(out, edges):

    if out["name"] not in edges:
        return out

    for ch in edges[out['name']]:
        out['children'].append(visit({'name': ch, "children": []}, edges))
    return out


def custom_tokenizer(st):
    return word_tokenize(
        st.lower()
        .encode("ascii", "ignore")
        .decode("ascii")
        .strip()
        .translate(str.maketrans(punctuation, " " * len(punctuation)))
        .translate(str.maketrans(digits, " " * len(digits))).strip()
    )


def generate_json(filename, keyword):
    ds = pd.read_csv(filename)
    ds = ds["Summary"].dropna().to_list()

    g = wordtree.search_and_draw(
        corpus=ds, keyword=keyword, tokenizer=custom_tokenizer)
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
        st = st.replace('"'+t+'"', '"'+t.split("-")[-1]+'"')
    return json.loads(st)
