from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
from pymongo import MongoClient

stop = 1
page = 0
dict_ = {"max": None,
         "min": None}
x = []
y = []
link = []
max_list = []
min_list = []
update = 'нет'
while update != "да":
    while stop != 0:

        main_link = "https://hh.ru"
        main_link_kurs = 'https://www.cbr.ru//'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        vacancy_name = 'data scientist'
        vacancy_name = vacancy_name.replace(' ', '+')
        response = requests.get(
            main_link + '/search/vacancy?area=1&clusters=true&enable_snippets=true&search_field=name&text=' + vacancy_name + '&page=' + str(
                page), headers=headers)
        response2 = requests.get(main_link_kurs, headers=headers)

        # Преобразуем в дом HTML
        soup = bs(response.text, 'html.parser')
        soup2 = bs(response2.text, 'html.parser')

        # начинаем поиск по тегам/классам/атрибута
        vacancy_list = soup.find('div', {'class': 'vacancy-serp'})  # список вакансий на странице
        vacancy_card = vacancy_list.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})  # блок с вакансией
        pprint(vacancy_card)
        vacancy_list = soup.find('div', {'class': 'vacancy-serp'})  # список вакансий на странице

        find_eur_usd_class = soup2.find_all('div', {'class': 'indicator_el_value mono-num'})  # поиск курса доллара
        kurs = []
        for i in find_eur_usd_class:
            find_ = i.getText()  # поиск курса
            find_ = find_[:-1]
            find_ = find_.replace(",", ".")
            find_ = float(find_)
            kurs.append(find_)

        # vacancy_name+

        for vacancy in vacancy_card:
            vacancy_name = vacancy.find('div', {"class": "vacancy-serp-item__info"})
            vacancy_name = vacancy_name.find('a', {"target": "_blank"}).getText()

            x.append(vacancy_name)

        # ссылка на вакансию
        for vacancy_href in vacancy_card:
            vacancy_link = vacancy_href.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
            link.append(vacancy_link)

        # зарплата мин / макс

        z = []

        for zp in vacancy_card:
            zarplata_in = zp.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            # обработка сумм:
            try:
                zarplata_in = zarplata_in.getText().replace(u'\xa0', ' ')
                z.append(zarplata_in)
            except:
                zarplata_in = 'Не указана'
                z.append(zarplata_in)


        # print(z)

        # обработка данных если рубли
        def salary_magic_ru(val1):
            in_val = ""
            in_val2 = ""
            e = 0
            for x in i:
                if e == 0:
                    if ('-' or 'о') in x:
                        e = 1
                    else:
                        try:
                            x = int(x)
                            x = str(x)
                        except:
                            x = ""
                        in_val += x
                        e = 0
                elif e == 1:
                    try:
                        if x == "Не указана":
                            x = ""
                        x = int(x)
                        x = str(x)
                    except:
                        x = ""
                    in_val2 += x
            return [(None if in_val2 == "" else int(in_val2)), (None if in_val == "" else int(in_val))]


        for i in z:
            if ("EUR" or "eur") in i:
                dict = salary_magic_ru(i)
                try:
                    max_list.append(dict[0] * kurs[2])
                except:
                    max_list.append(0)
                try:
                    min_list.append(dict[1] * kurs[2])
                except:
                    min_list.append(0)

            elif ("USD" or "usd") in i:
                dict = salary_magic_ru(i)
                try:
                    max_list.append(dict[0] * kurs[0])
                except:
                    max_list.append(0)
                try:
                    min_list.append(dict[1] * kurs[0])
                except:
                    min_list.append(0)
            else:
                dict = salary_magic_ru(i)
                max_list.append(dict[0])
                min_list.append(dict[1])

        # Company_name
        try:
            for vacancy2 in vacancy_card:
                Company_name = vacancy2.find_next('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText()
                y.append(Company_name)
        except:
            Company_name = "None"
            y.append(Company_name)

        # проверка на конец страницы
        actual_page = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if actual_page == None:
            stop = 0
        else:
            page += 1

    dict_ = {"vacancy_name": x, "Company_name": y, "max": max_list,
             "min": min_list, "link": link, "Source": "НH.RU"}
    print(len(x), len(y), len(max_list), len(min_list), len(link))
    df = pd.DataFrame(dict_)

    # Добавление данных в БД Mongo

    # Задание 1

    # настройка сервера MongoDB
    client = MongoClient('localhost', 27017)

    # Подключение к БД
    db = client['test_database']
    # Указатель на коллекцию
    HH_DB = db.test_collection
    hh_db = db.HH_DB

    # Обновить БД?
    update = input("Обновить БД? да/нет")
    if update == "нет":

        list = []
        for t, i in enumerate(x):
            # создание словарей для добавления
            list.append({"vacancy_name": x[t], "Company_name": y[t], "max": max_list[t], "min": min_list[t], "link": link[t],
                         "Source": "НH.RU"})
        hh_db.insert_many(list)
        update = "да"

    # Задание 3
    elif update == "да":
        list = []
        for t, i in enumerate(x):
            # создание словарей для добавления
            list.append(
                {"vacancy_name": x[t], "Company_name": y[t], "max": max_list[t], "min": min_list[t], "link": link[t],
                 "Source": "НH.RU"})
        hh_db.update_many({}, list , upsert=True)
        update = "да"

    # Задание 2

    def find_vacancy(val_find, hh_db):
        for user in hh_db.find({'$or': [{'max': {'$gt': val_find}}, {'min': {'$gt': val_find}}]}):
            return print(f"{user.get('vacancy_name')}\n{user.get('Company_name')}")

    find_vacancy(int(input("Введите сумму, в рамках которой, зарплата на вакансии будет больше: ")), hh_db)

df.to_excel(r"C:\Users\Nekit\Desktop\GEEK BRAINS\Методы сбора и обработки данных из сети Интернет\Vacancy.xlsx")
