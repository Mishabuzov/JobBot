import telebot
import time
from sys import argv as args
from utils import get_vectorizer, get_truncater, get_index, \
    get_vacancies_info_dict


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
    bot.send_message(message.chat.id, GREETING_MSG)


@bot.message_handler(commands=['set_results_count'])
def change_results_count(message):
    msg = f"Currently {RETURN_VACANCIES_COUNT} are returning. print how much you "
    # bot.send_message(message.chat.id)


@bot.message_handler(content_types=['text'])
def send_text(message):
    text = message.text.lower().strip()

    if text == '':
        return

    start = time.time()
    relevant_vacancies = process_query(text)
    print(f"Query processed by {time.time() - start} sec.")
    for vacancy in relevant_vacancies:
        bot.send_message(message.chat.id, vacancy, parse_mode='Markdown')

    # TODO: Change to regexp tokenizer check. If it is empty -> warning!
    # if text in punctuation:
    #     bot.send_message(message.chat.id,
    #                      'please do not construct your query only '
    #                      'from specsymbols')
    #
    #
    #     bot.send_message(message.chat.id, 'Привет, мой создатель')
    # elif message.text == 'Пока':
    #     bot.send_message(message.chat.id, 'Прощай, создатель')


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


# TODO: Добавить ручное удаление цифр + spellchecker
def process_query(query):
    # query = ''.join([i for i in query if not i.isdigit()])
    query = vectorizer.transform([query])
    query = svd.transform(query)
    relevant_ids = hnsw_index.knn_query(query, k=RETURN_VACANCIES_COUNT)
    response_vacancies = map_id_to_vacancy(relevant_ids[0][0])
    return response_vacancies


# TODO: Сообщения на вывод +

if __name__ == '__main__':
    vectorizer = get_vectorizer()
    svd = get_truncater()
    hnsw_index = get_index()
    # hnsw_index.set_ef(5)
    id_to_vacancy = get_vacancies_info_dict()
    bot.polling()

