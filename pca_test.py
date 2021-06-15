from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics.cluster import (
    completeness_score,
    homogeneity_score,
    adjusted_rand_score,
)
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import os


from string import punctuation

import random

import numpy as np

from time import time

sw = set(stopwords.words("english"))
sw.add("removed")
punct = punctuation
lemmatizer = WordNetLemmatizer()
SVD_DIMENSIONS = 10
VEC_MIN_DOCS = 3
N_WORDS = 10


def analyze_text(text):
    # remove punctuation and tokenize

    tokens = word_tokenize(
        text.lower()
        .encode("ascii", "ignore")
        .decode("ascii")
        .strip()
        .translate(str.maketrans(punctuation, " " * len(punctuation)))
    )
    stem = []
    # lemmatize, remove stop words
    for word in tokens:
        if word not in sw:
            word = lemmatizer.lemmatize(word)
            stem.append(word)
    return stem


def work(X):

    # with open("comments_science") as corpus:
    #     X = eval(corpus.read())

    vectorizer = TfidfVectorizer(
        analyzer=analyze_text, min_df=VEC_MIN_DOCS, stop_words="english"
    )

    s0 = time()
    print("Fitting the vectorizer... ")
    X_train = vectorizer.fit_transform(X)

    vec_shape = X_train.shape

    print("Dataset in original space has shape %s" % str(vec_shape))

    s0 = time()
    svd = TruncatedSVD(n_components=SVD_DIMENSIONS)
    normalizer = Normalizer(copy=False)
    pipeline = make_pipeline(svd, normalizer)

    print("Fitting SVD/Normalizer pipeline... ")
    X_train = pipeline.fit_transform(X_train)
    print("Done in %.3lfs" % (time() - s0))

    dimred_shape = X_train.shape

    mean = np.mean(X_train, axis=0).reshape(1, -1)

    print(mean)

    # print relevant terms for each cluster
    original_space_centroids = svd.inverse_transform(mean)
    order_centroids = original_space_centroids.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for ind in order_centroids[0, :N_WORDS]:
        print(" %s" % terms[ind])

    # for i in range(N_CLUSTERS):
    #     print("Cluster %d:" % i)
    #     word_weight_dic = {}
    #     for ind in order_centroids[i, :N_WORDS]:
    #         print(" %s" % terms[ind])
    #         word_weight_dic[terms[ind]] = vectorizer.idf_[ind]

    #     print()
    #     wordcloud = WordCloud(background_color="white").generate_from_frequencies(
    #         word_weight_dic
    #     )

    #     plt.subplot(1, N_CLUSTERS, i + 1)
    #     plt.title("Cluster %d" % (i + 1), pad=20)
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    # plt.show()


if __name__ == "__main__":
    ds = []
    f = open("dataset.csv", "r")
    for line in f.readlines():
        ds.append(line.split(",")[-1].strip())

    work(ds)