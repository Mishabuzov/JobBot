from crawl_and_build.vacancies_preprocessor import preprocess_vacancies
from crawl_and_build.vacancies_indexer import create_search_structures
from crawl_and_build.vacancies_crawler import crawl_vacancies
from sys import argv as args

def create_data_and_structures(crawl=False, preprocess=False, create_index=True):
    if crawl:
        crawl_vacancies()
    if preprocess:
        preprocess_vacancies()
    if create_index:
        create_search_structures()


if __name__ == '__main__':
    # parse args
    is_need_crawl, is_need_to_preprocess, is_need_to_index = True, True, True
    if args[1].strip().lower() == 'false':
        is_need_crawl = False
    if args[2].strip().lower() == 'false':
        is_need_to_preprocess = False
    if args[3].strip().lower() == 'false':
        is_need_to_index = False

    # start pipeline
    create_data_and_structures(is_need_crawl, is_need_to_preprocess, is_need_to_index)
