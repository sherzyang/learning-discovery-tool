import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
from flask import Flask, request, render_template, jsonify

import os
import numpy as np
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine, cdist
import requests

app = Flask(__name__, static_url_path="")
    
# with open(r"data/new_corpus.pkl", "rb") as input_file:
#     new_corpus = pickle.load(input_file)

def download_and_open(url, mode='rb', folder='data'):
    """Downloads the specified file if it isn't already downloaded, then opens it."""
    filename = os.path.basename(url)
    pathname = os.path.join(folder, filename)
    if not os.path.exists(pathname):
        response = requests.get(url)
        with open(pathname, 'wb') as f:
            f.write(response.content)
    return open(pathname, mode)

with download_and_open(r"https://text-ascent.s3-us-west-2.amazonaws.com/new_corpus.pkl", "rb") as input_file:
    new_corpus = pickle.load(input_file)
    
# with open (r"data/dictionary.pkl", "rb") as input_file: 
#     dictionary = pickle.load(input_file)

with download_and_open(r"https://text-ascent.s3-us-west-2.amazonaws.com/dictionary.pkl", "rb") as input_file: 
     dictionary = pickle.load(input_file)

@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')

def load_vectorizer(pickle_file='https://text-ascent.s3-us-west-2.amazonaws.com/vectorizer.pkl'):
    """Loads the trained TF/IDF vectorizer."""
    with download_and_open(pickle_file, 'rb') as f:
        return pickle.load(f)
    
def load_corpus_vectors(pickle_file='https://text-ascent.s3-us-west-2.amazonaws.com/corpus_vectors.pkl'):
    """Loads the corpus vectors."""
    with download_and_open(pickle_file, 'rb') as f:
        return pickle.load(f)
    
def get_vocab_arr(vec):
    n_features = len(vec.vocabulary_)
    vocab_arr = np.empty(n_features, dtype=object)
    for word, idx in vec.vocabulary_.items():
        vocab_arr[idx] = word
    return vocab_arr

def get_top_k_vector(vector, feature_ranking, k=20):
    """Return the top k vector according to feature_ranking."""
    return vector[:, feature_ranking[:k]]

def vectorize_text(text):
    vec = load_vectorizer()
    corpus_vectors = load_corpus_vectors().toarray()
    sample_vector = vec.transform([text]).toarray()
    feature_ranking = np.argsort(sample_vector[0])[::-1]
    vocab_arr = get_vocab_arr(vec)
    
    distances = cdist(
    get_top_k_vector(sample_vector, feature_ranking),
    get_top_k_vector(corpus_vectors, feature_ranking),
    )
    
    nearest_article_idxs = np.argsort(distances)
    nearest_articles = new_corpus.loc[nearest_article_idxs[0], :]
    top_10 = nearest_articles[:10]
    top_df = top_10.sort_values(['score'])
    article_num = str(nearest_articles[:1].index)
    article_num_str = article_num.strip("Int64Index([], dtype='int64')")
    article_num_final = int(article_num_str)
     
    return nearest_articles.loc[article_num_final, 'content']

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return a new article."""
    data = request.json
    data = str(data)
    result = vectorize_text(data)
    return jsonify(result)


