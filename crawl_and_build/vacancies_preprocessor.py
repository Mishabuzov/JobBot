import re
import pickle
import nltk
nltk.download("stopwords")
from nltk import regexp_tokenize
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import time
import os
import json
from pathlib import Path
from utils import RAW_VACANCIES_DIR, CLEANED_VACANCIES_DIR, \
    VACANCIES_INFO_SER_PATH, STRUCTURES_DIR


mystem = Mystem()
stopwords = set(stopwords.words('russian')).union(set(stopwords.words('english')))
min_word_length = 2
filter_regexp = r'(?u)\b\w{2,}\b'


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in stopwords
              and token != " "
              and token.strip() not in punctuation
              and token.isalpha()
              and len(token) >= min_word_length]
    # additional filter for punct. and others.
    tokens = regexp_tokenize(" ".join(tokens), filter_regexp)
    return " ".join(tokens)


id_info = {}
vacancy_id = 0
def process_vacancies(vacancies, filename_to_save):
    def save_vacancy_info(vacancy, description):
        global vacancy_id
        id_info[vacancy_id] = {}

        def extract_salary(salary):
            if salary is None:
                return ''
            salary_from = f"from {salary['from']}" if salary['from'] is not None else ''
            salary_to = f"to {salary['to']}" if salary['to'] is not None else ''
            currency = salary['currency'] if salary['currency'] is not None else ''

            if salary_from != '' or salary_to != '':
                return f"{salary_from} {salary_to} {currency}".strip()
            return ''

        id_info[vacancy_id]['description'] = description[:500]
        id_info[vacancy_id]['name'] = vacancy['name']
        id_info[vacancy_id]['area'] = vacancy['area']['name']
        id_info[vacancy_id]['salary'] = extract_salary(vacancy['salary'])
        id_info[vacancy_id]['url'] = vacancy['url'] if vacancy['url'] is not None else ''
        vacancy_id += 1

    print(filename_to_save)
    test_corpus = []
    start = time.time()
    for i, vacancy in enumerate(vacancies):
        cleaned_description = cleanhtml(vacancy['description'])
        raw_vacancy_text = f"{vacancy['name']} {vacancy['area']['name']} {cleaned_description}"
        test_corpus.append(preprocess_text(raw_vacancy_text))
        save_vacancy_info(vacancy, cleaned_description)

        if (i + 1) % 1000 == 0:
            print(f'{i + 1} vacancies ({round((i + 1) / len(vacancies) * 100, 2)}%) are processed, \
                {(time.time() - start) // 60} minutes are spent')

    with open(filename_to_save, "w", encoding="utf-8") as processed_file:
        for i, vacancy in enumerate(test_corpus):
            if i < len(vacancies) - 1:
                processed_file.write(vacancy + '\n')
            else:
                processed_file.write(vacancy)

Path(STRUCTURES_DIR).mkdir(parents=True, exist_ok=True)
def save_vacancies_main_info():
    """Save dict. with main data about each vacancy."""
    with open(VACANCIES_INFO_SER_PATH, 'wb') as f:
        pickle.dump(id_info, f)


# if __name__ == '__main__':
def preprocess_vacancies():
    Path(CLEANED_VACANCIES_DIR).mkdir(parents=True, exist_ok=True)
    for vacancy_file in os.scandir(RAW_VACANCIES_DIR):
        with open(vacancy_file.path) as json_file:
             vacancies = json.load(json_file)
        filename_to_save = f"{CLEANED_VACANCIES_DIR}/{vacancy_file.name.replace('.json', '.txt')}"
        process_vacancies(vacancies, filename_to_save)
    save_vacancies_main_info()
