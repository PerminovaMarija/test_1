import requests
import re
import schedule
import time
from bs4 import BeautifulSoup


def get_data(cur):
    if cur == 'RUB':
        res = 1.0
        """ устанавливаем значение для рубля """
    else:
        response = requests.get('https://www.cbr.ru/currency_base/daily/')
        """ обращаемся к странице с курсами всех валют к рублю """
        soup = BeautifulSoup(response.text, 'lxml')
        td = soup.find('td', string=re.compile(cur))
        """ находим строку с той валютой, которая нас интересует """
        tr = str(td.find_parent())
        new_soup = BeautifulSoup(tr, 'lxml')
        lst = [elem.string for elem in new_soup.find_all('td')]
        res = float(lst[4].replace(',', '.'))
        """ из всей полученной информации по валюте, оставляем только курс,
            меняем символ запятой на точку для преобразования к float """
    return res


def rate(a, b):
    res_rate = "%.4f" % (get_data(a) / get_data(b))
    """ считем курс двух валют друг к другу с точностью 4 знака после точки """
    return res_rate


def result(x: list):
    """ принимает список валютных пар, которые нужно отслеживать """
    res = {}
    for el in x:
        params = el.split('-')
        res_params = rate(params[0], params[1])
        """ считаем курс всех валютных пар по очереди """
        res[el] = res_params
    body = {'rate': res}
    """ в реальности здесь скорее будет не body, а part_body, как часть json-строки,
        которая потом отправится poct-запросом на нужный endpoint """
    # requests.post('api_endpoint', body)
    """ отправляем post-запрос, с полученными данными """


def job():
    result(['RUB-EUR', 'EUR-USD', 'EUR-KZT'])
    """ указываем требуемые валютные пары  """


schedule.every().day.at("11:32").do(job)
""" запускаем повтор ежедневно в 11.32, поскольку курсы обновляются в 11.30
    (нужно учитывать, что это курсы для следующего дня)  """

while True:
    schedule.run_pending()
    time.sleep(1)


