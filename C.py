from celery import Celery
from random import randint, choice
import requests
from bs4 import BeautifulSoup

# попытка зделать асинхронность.


app = Celery('tasks',  broker='') #сюда адрес брокера.              #'redis://localhost:6379/0'


@app.task
def f_hed():
    'авось... создаст достаточную имитацию разных пользователей'
    a = ['text/dfb', '12ghy', '44*ss', '77', 'ghd', 'dgbfds']
    b = ['Mozi', 'Ian', 'UFO', 'AAA']
    c = ['Gecko', 'sccscscscsc', 'Q', 'GGG']

    acc = f'{choice(a)}/ css,{randint(1, 111)} / *;{choice(b)} = {randint(7,777)}'
    u_a = f'{choice(c)}/{randint(10,100)} ({choice(b)} {randint(5, 555)}; {choice(c)};' \
          f' x{randint(1, 88)}; rv:136.0) {choice(a)}/20100101 {choice(c)}x/{randint(1, 100)}.0'
    rez = {'Accept': acc, 'User-Agent': u_a}
    return rez



@app.task
def etap_1(a):
    'принимает номер страницы, в формате str. возвращает словарь в котором ключи это ссылки на печатные формы, а значения  - XML.'
    stroka = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=' + a[0]

    data_1 = requests.get(stroka, headers=f_hed.delay()).text
    data_2 = BeautifulSoup(data_1, 'lxml')

    spisok_1 = data_2.find_all('img', src="/epz/static/img/icons/icon_print_small.svg")

    spisok_2 = ['https://zakupki.gov.ru/' + i.parent.get('href') for i in spisok_1]

    spisok_3 = dict()
    for i in spisok_2:
        s = i.split('/')
        s[len(s) - 1] = s[len(s) - 1].split('?')
        s[len(s) - 1][0] = 'viewXml.html'
        s = '/'.join(s[:len(s) - 1:]) + '/' + s[len(s) - 1][0] + '?' + s[len(s) - 1][1]
        spisok_3[i] = s

    return spisok_3



@app.task
def etap_2(stroka):
    'получает ссылку на xml, возвращает содержимое  тега "publishDTInEIS", или None.'
    teg = 'publishDTInEIS'
    try:
        data = requests.get(stroka[0], headers=f_hed.delay()).text
        data_2 = BeautifulSoup(data, 'xml')
        rez = data_2.find(teg).text
    except:
        return None
    if len(rez) == 29:
        return rez
    else:
        return None



@app.task
def obrabotka_stranihi(s):
    'обработка страницы. получает на вход номер страницы, в формате str. выдаёт словарь'
    slovar_1 = etap_1.apply_async(s[0])
    slovar_2 = dict()
    for i in slovar_1:
        slovar_2[i] = etap_2.apply_async([slovar_1[i]])
    return slovar_2



print(1)
a = obrabotka_stranihi.apply_async(['1'])
for i in a:
    print(i, a[i], '\n')

print('-'*100, '\n', 2)
b = obrabotka_stranihi.apply_async(['2'])
for i in b:
    print(i, b[i], '\n')