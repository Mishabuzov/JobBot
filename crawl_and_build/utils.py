VACANCIES_DIR = "crawl_and_build/vacancies_data"
RAW_VACANCIES_DIR = f"{VACANCIES_DIR}/classified_vacancies"
CLEANED_VACANCIES_DIR = f"{VACANCIES_DIR}/cleaned_vacancies"

STRUCTURES_DIR = "ser_structures"
VECTORIZER_SER_PATH = f'{STRUCTURES_DIR}/TfidfVectorizer_ser.pickle'
TRUNCATER_SER_PATH = f'{STRUCTURES_DIR}/SVD_ser.pickle'
INDEX_SER_PATH = f'{STRUCTURES_DIR}/hnsw_index_cos'
VACANCIES_INFO_SER_PATH = f'{STRUCTURES_DIR}/id_info_ser.pickle'
