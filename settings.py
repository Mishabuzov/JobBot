import pickle
import hnswlib

RAW_VACANCIES_DIR = "crawl_and_build/vacancies_data/classified_vacancies"
CLEANED_VACANCIES_DIR = "crawl_and_build/vacancies_data/cleaned_vacancies"
STRUCTURES_DIR = "ser_structures"

VECTORIZER_SER_PATH = f'{STRUCTURES_DIR}/TfidfVectorizer_ser.pickle'
TRUNCATER_SER_PATH = f'{STRUCTURES_DIR}/SVD_ser.pickle'
INDEX_SER_PATH = f'{STRUCTURES_DIR}/hnsw_index_cos'
VACANCIES_INFO_SER_PATH = f'{STRUCTURES_DIR}/id_info_ser.pickle'

# TODO: Make a class.
def __get_structure(path):
    with open(path, 'rb') as f:
        structure = pickle.load(f)
    return structure

def get_vectorizer():
    return __get_structure(VECTORIZER_SER_PATH)

def get_truncater():
    return __get_structure(TRUNCATER_SER_PATH)

def get_vacancies_info_dict():
    return __get_structure(VACANCIES_INFO_SER_PATH)

# todo: set some deafult value constant instead of hardcode
def get_index():
    p = hnswlib.Index(space='cosine', dim=1500)
    p.load_index(INDEX_SER_PATH)
    return p
