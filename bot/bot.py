import telebot
from sys import argv as args
import time
from utils import get_vectorizer, get_truncater, get_index, \
    get_vacancies_info_dict

counts = {}
with open(args[1].strip(), 'r') as token_file:
    TOKEN = token_file.read().strip()
bot = telebot.TeleBot(TOKEN)

GREETING_MSG = "Hi, I am looking for vacancies throughout Russia " \
               "in the fields of IT, medicine and marketing.\n" \
               "I return the 5 most appropriate ones to your request.\n" \
               "To change this number, run the command: /set_results_count :value:\n" \
               "In order to start search just type your query."

RETURN_VACANCIES_COUNT = 5


@bot.message_handler(commands=['start'])
def start_message(message):
    counts[message.chat.id] = RETURN_VACANCIES_COUNT
    bot.send_message(message.chat.id, GREETING_MSG)


@bot.message_handler(commands=['set_results_count'])
def change_results_count(message):
    _, count = message.text.split(' ')
    try:
        count = int(count)
    except:
        bot.send_message(message.chat.id, "To change this number, run the command: /set_results_count :value:\n")
        return

    counts[message.chat.id] = count
    bot.send_message(message.chat.id, f'Return vacancies count is changed to {counts[message.chat.id]}')


@bot.message_handler(content_types=['text'])
def send_text(message):
    text = message.text.lower().strip()

    if text == '':
        return

    relevant_vacancies = process_query(text, counts[message.chat.id])
    for vacancy in relevant_vacancies:
        bot.send_message(message.chat.id, vacancy, parse_mode='Markdown')


def map_id_to_vacancy(ids):
    response_vacancies = []
    for id in ids:
        vacancy_string = f"*{id_to_vacancy[id]['name']} "
        vacancy_string += f"({id_to_vacancy[id]['area']})*\n"
        salary = id_to_vacancy[id]['salary']
        vacancy_string += f"_salary: \t{salary if salary != '' else 'not mentioned'}_\n\n"
        vacancy_string += f"{id_to_vacancy[id]['description'][0:100]}...\n"
        vacancy_string += f"{id_to_vacancy[id]['url']}"
        response_vacancies.append(vacancy_string)
    return response_vacancies


def process_query(query, K):
    # query = ''.join([i for i in query if not i.isdigit()])
    start = time.time()
    query = vectorizer.transform([query])
    query = svd.transform(query)
    relevant_ids = hnsw_index.knn_query(query, k=K)
    response_vacancies = map_id_to_vacancy(relevant_ids[0][0])
    print(f'Query is processed for {time.time() - start}')
    response_vacancies.reverse()
    return response_vacancies


if __name__ == '__main__':
    vectorizer = get_vectorizer()
    svd = get_truncater()
    hnsw_index = get_index()
    # hnsw_index.set_ef(5)
    id_to_vacancy = get_vacancies_info_dict()
    bot.polling()
