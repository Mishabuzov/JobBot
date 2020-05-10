# https://api.hh.ru/vacancies?per_page=100&area=112
import requests
import json
import time
from pathlib import Path
from settings import RAW_VACANCIES_DIR

BASE_VACANCY_URL = 'https://api.hh.ru/vacancies'
LIMIT_PAGES = 20  # Limit is set by hh API.
LIMIT_VACANCIES_PER_FILE = 50000


def get_deepest_area_ids(area, subareas_ids):
    if len(area['areas']) > 0:
        for sub_area in area['areas']:
            get_deepest_area_ids(sub_area, subareas_ids)
    else:
        subareas_ids.add(int(area['id']))


areas_ids = set()
def parse_areas():
    response = requests.get('https://api.hh.ru/areas')
    if response.status_code == 200:
        all_areas = response.json()
        for area in all_areas:
            if area['name'] == "Россия":  # Extract all Russian regions' ids.
                get_deepest_area_ids(area, areas_ids)


def process_vacancy(raw_vacancy_description):
    """Filter redundant vacancy fields"""
    return {'id': raw_vacancy_description['id'],
            'name': raw_vacancy_description['name'],
            'area': raw_vacancy_description['area'],
            'salary': raw_vacancy_description['salary'],
            'address': raw_vacancy_description['address'],
            'experience': raw_vacancy_description['experience'],
            'employment': raw_vacancy_description['employment'],
            'description': raw_vacancy_description['description'],
            'employer': raw_vacancy_description['employer'],
            'published_at': raw_vacancy_description['published_at'],
            'url': raw_vacancy_description['alternate_url']}

VACANCIES_SAVING_DIR = f""
specializations = {'1': 'IT', '13': 'medicine', '17': 'sellings'}
Path(RAW_VACANCIES_DIR).mkdir(parents=True, exist_ok=True)  # check if saving dir is created.
def save_vacancies(vacancies, spec_id):
    with open(f'{RAW_VACANCIES_DIR}/{specializations[spec_id]}_vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


# if __name__ == '__main__':
def crawl_vacancies():
    parse_areas()
    print(f'{len(areas_ids)} areas are extracted')

    start_time = time.time()

    for spec_id in specializations:
        vacancies = []
        print(f"Parsing {specializations[spec_id]} vacancies")
        for area_id in sorted(areas_ids):
            for page_num in range(LIMIT_PAGES):
                response = requests.get(
                    f'{BASE_VACANCY_URL}?per_page=100&page={page_num}&area={area_id}&specialization={spec_id}'
                )
                if response.status_code == 200:
                    new_vacancies = response.json()['items']

                    if len(new_vacancies) == 0:  # exit if vacancies are over.
                        break

                    for vacancy in new_vacancies:
                        detailed_responce = requests.get(f'{BASE_VACANCY_URL}/{vacancy["id"]}')

                        if detailed_responce.status_code == 200:
                            vacancies.append(process_vacancy(detailed_responce.json()))

            print(f"{specializations[spec_id]} area:", f"{len(vacancies) // 1000}k vacancies are parsed.",
                  f'{round((time.time() - start_time) / 60, 2)} minutes are spent')

            if len(vacancies) >= LIMIT_VACANCIES_PER_FILE:  # limit number of vacancies by concrete area.
                print(f"{area_id} is the last area_id for the #{file_num} .json file")
                save_vacancies(vacancies, spec_id)
                vacancies = []
                break

        if len(vacancies) != 0:  # In case if all the areas are iterated, but limit was not reached.
            save_vacancies(vacancies, spec_id)
