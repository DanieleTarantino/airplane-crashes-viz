from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

from string import punctuation, digits


import numpy as np


sw = set(stopwords.words("english"))
sw.add("removed")
punct = punctuation
lemmatizer = WordNetLemmatizer()
SVD_DIMENSIONS = 10
VEC_MIN_DOCS = 3
N_WORDS = 10


def wordcloud_from_cvs(filename, nwords, size):
    ds = pd.read_csv(filename)
    ds = ds["Summary"].dropna().to_list()
    return work(ds, nwords, size)


def analyze_text(text):
    # remove punctuation and tokenize

    tokens = word_tokenize(
        text.lower()
        .encode("ascii", "ignore")
        .decode("ascii")
        .strip()
        .translate(str.maketrans(punctuation, " " * len(punctuation)))
        .translate(str.maketrans(digits, " " * len(digits)))
    )
    stem = []
    # lemmatize, remove stop words
    for word in tokens:
        if word not in sw:
            word = lemmatizer.lemmatize(word)
            stem.append(word)
    return stem


def work(X, nwords, size):

    vectorizer = TfidfVectorizer(
        analyzer=analyze_text, min_df=VEC_MIN_DOCS, stop_words="english"
    )

    X_train = vectorizer.fit_transform(X)
    svd = TruncatedSVD(n_components=SVD_DIMENSIONS)
    normalizer = Normalizer(copy=False)
    pipeline = make_pipeline(svd, normalizer)

    X_train = pipeline.fit_transform(X_train)

    mean = np.mean(X_train, axis=0).reshape(1, -1)

    # print relevant terms for each cluster
    original_space_centroids = svd.inverse_transform(mean)
    order_centroids = original_space_centroids.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()

    x = []
    y = []

    for idx in order_centroids[0, :nwords]:
        x.append(terms[idx])
        y.append(original_space_centroids[0][idx])
    y = np.rint(np.interp(y, [min(y), max(y)], size)).tolist()

    return list(zip(x, y))


if __name__ == "__main__":
    ds = pd.read_csv("dataset.csv")
    ds = ds["Summary"].dropna().to_list()
    work(ds, 10)
