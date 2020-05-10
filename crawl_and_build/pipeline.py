from crawl_and_build.vacancies_preprocessor import preprocess_vacancies
from crawl_and_build.vacancies_indexer import create_search_structures
from crawl_and_build.vacancies_crawler import crawl_vacancies

def create_data_and_structures(crawl=False, preprocess=False, create_index=True):
    if crawl:
        crawl_vacancies()
    if preprocess:
        preprocess_vacancies()
    if create_index:
        create_search_structures()

# TODO: Add environments!
if __name__ == '__main__':
    create_data_and_structures()
