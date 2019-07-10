import pickle
import os
import requests

import numpy as np
import pandas as pd
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine, cdist

def download_and_open(url, mode='rb', folder='data'):
    """Downloads the specified file if it isn't already downloaded, then opens it."""
    filename = os.path.basename(url)
    pathname = os.path.join(folder, filename)
    if not os.path.exists(pathname):
        response = requests.get(url)
        with open(pathname, 'wb') as f:
            f.write(response.content)
    return open(pathname, mode)

with download_and_open(r"https://text-ascent.s3-us-west-2.amazonaws.com/clean_df.pkl", "rb") as input_file:
    clean_df = pickle.load(input_file)

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

def top_k_text(text, k=50):
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
    nearest_articles = clean_df.loc[nearest_article_idxs[0], :]
    
    top_k = nearest_articles[:k].copy()
    top_k['summary'] = clean_df['summary']
    top_k['title'] = clean_df['title']
    top_k['url'] = clean_df['url']
    top_k['_id'] = clean_df['_id']
                                        
#     top_k['summary'] = top_k['content'].apply(lambda text: ' '.join(text.split()[:20]))
#     top_k['title'] = top_k['content'].apply(lambda text: ' '.join(text.split()[:4]).capitalize())
#     top_k['url'] = top_k['title'].apply(lambda title: f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}')
#     top_k['_id'] = range(k)  # will be replaced with ObjectID from MongoDB
    top_k['i'] = range(k)  # won't change
    top_k = top_k.sort_values(['score'])
    top_k['style'] = "display: none"
    top_k.loc[(top_k['i'] >= 22) & (top_k['i'] < 27), 'style'] = ""
    return top_k
