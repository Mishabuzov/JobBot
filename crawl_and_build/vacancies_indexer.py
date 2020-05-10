import os
import pickle
import hnswlib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from utils import CLEANED_VACANCIES_DIR, VECTORIZER_SER_PATH, \
    TRUNCATER_SER_PATH, INDEX_SER_PATH, STRUCTURES_DIR


def read_vacancies():
    text_vacancies = []
    for vacancy_file in os.scandir(CLEANED_VACANCIES_DIR):
        with open(vacancy_file.path, "r") as data_file:
            for line in data_file:
                text_vacancies.append(line.strip())
    return text_vacancies


def vectorize_text(text_vacancies, min_df=5, save_vectorizer=True):
    vectorizer = TfidfVectorizer(min_df=min_df)
    X = vectorizer.fit_transform(text_vacancies)
    print(f"Vectorized matrix of all vacancies has shape: {X.shape}")
    if save_vectorizer:
        with open(VECTORIZER_SER_PATH, 'wb') as f:
            pickle.dump(vectorizer, f)
    return X


def truncate_vectors(X, n_components=1500, save_truncater=True):
    svd = TruncatedSVD(n_components=n_components)
    Xk = svd.fit_transform(X)
    print(f"Truncated matrix of all vacancies has shape: {Xk.shape}")
    print(f"Truncated matrix covers "
          f"{round(sum(svd.explained_variance_ratio_), 2) * 100}% of variance")
    if save_truncater:
        with open(TRUNCATER_SER_PATH, 'wb') as f:
            pickle.dump(svd, f)
    return Xk


def build_search_index(Xk, ef_construction=1000, M=90, save_index=True):
    p = hnswlib.Index(space='cosine', dim=Xk.shape[1])
    p.init_index(max_elements=Xk.shape[0],
                 ef_construction=ef_construction,
                 M=M)
    p.add_items(Xk)
    if save_index:
        p.save_index(INDEX_SER_PATH)


# if __name__ == '__main__':
def create_search_structures():
    Path(STRUCTURES_DIR).mkdir(parents=True, exist_ok=True)
    text_vacancies = read_vacancies()
    X = vectorize_text(text_vacancies)
    Xk = truncate_vectors(X)
    del X  # clean memory a little
    build_search_index(Xk)
