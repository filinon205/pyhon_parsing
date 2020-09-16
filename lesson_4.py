from pprint import pprint
from lxml import html
import requests
from datetime import datetime
from pymongo import MongoClient
# настройка сервера MongoDB
client = MongoClient('localhost', 27017)

# Подключение к БД
db = client['test_database']
# Указатель на коллекцию
news_DB = db.test_collection
news_db = db.news_DB

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

dashboard_news = dom.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])/a/text()''')

dashboard_link = dom.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])/a/@href''')

fin_date = []
source = "Lenta.ru"

for i in range(len(dashboard_news)):
    dashboard_news[i] = dashboard_news[i].replace(u'\xa0', u' ')
    print(dashboard_news[i])

for item in dashboard_link:
    response2 = requests.get(main_link + item)
    fin_date.append("no date")
    path_list = html.fromstring(response2.text)
    dashboard_date2 = path_list.xpath('''//div[@class="b-topic__info"]//time[@class='g-date']/@datetime''')
    for z, i in enumerate(dashboard_date2):
        date = dashboard_date2[0]
        date = date.split("T")
        fin_date.append(date[0])

list_news = []

for t, i in enumerate(dashboard_news):
# создание словарей для добавления
    list_news.append({"news_name": dashboard_news[t], "source": "Lenta.ru", "link": main_link + dashboard_link[t], "date": fin_date[t]})
#добавление в БД
news_db.insert_many(list_news)


#news.mail.ru ---------------------------------------------------------------------------------------

main_link = 'https://news.mail.ru/'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

dashboard_news = dom.xpath('''(//div[@class='js-module']//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text() |
                                            //a[@class = "list__text"])/text()''')

dashboard_link = dom.xpath('''(//div[@class='js-module']//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text() |
                                            //a[@class = "list__text"])/@href''')

fin_date2 = []
source = []

for i in range(len(dashboard_news)):
    dashboard_news[i] = dashboard_news[i].replace(u'\xa0', u' ')
    print(dashboard_news[i])

for e, item in enumerate(dashboard_link):
    response2 = requests.get(item)
    path_list = html.fromstring(response2.text)
    dashboard_date2 = path_list.xpath('''//span[@class='note__text breadcrumbs__text js-ago']/@datetime''')

    link = path_list.xpath('''//div[@class="breadcrumbs breadcrumbs_article js-ago-wrapper"]//span[@class="link__text"]/../@href''')
    source.append(link[0])
    for z, i in enumerate(dashboard_date2):
        date = dashboard_date2[0]
        date = date.split("T")
        fin_date2.append(date[0])

list_news2 = []

for t, i in enumerate(dashboard_news):
# создание словарей для добавления
    list_news2.append({"news_name": dashboard_news[t], "source": source[t], "link": dashboard_link[t], "date": fin_date2[t]})
#добавление в БД
news_db.insert_many(list_news2)

#yandex.ru ---------------------------------------------------------------------------------------

main_link = 'https://yandex.ru/news/rubric/personal_feed'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

dashboard_news = dom.xpath('''(//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/article[@class="mg-card news-card news-card_double news-card_type_image mg-grid__item mg-grid__item_type_card"]//h2 |
                               //div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//article[@class="mg-card news-card news-card_single news-card_type_image mg-grid__item mg-grid__item_type_card"]//h2)/text()''')

dashboard_link = dom.xpath('''(//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/article[@class="mg-card news-card news-card_double news-card_type_image mg-grid__item mg-grid__item_type_card"]//a |
                               //div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//article[@class="mg-card news-card news-card_single news-card_type_image mg-grid__item mg-grid__item_type_card"]//a)/@href''')

source2 = dom.xpath('''(//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/article[@class="mg-card news-card news-card_double news-card_type_image mg-grid__item mg-grid__item_type_card"]//span[@class="mg-card-source__source"]/a |
                               //div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//article[@class="mg-card news-card news-card_single news-card_type_image mg-grid__item mg-grid__item_type_card"]//span[@class="mg-card-source__source"]/a)/text()''')

dashboard_date = dom.xpath('''(//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/article[@class="mg-card news-card news-card_double news-card_type_image mg-grid__item mg-grid__item_type_card"]//span[@class="mg-card-source__time"] |
                               //div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//article[@class="mg-card news-card news-card_single news-card_type_image mg-grid__item mg-grid__item_type_card"]//span[@class="mg-card-source__time"])/text()''')

for i in range(len(dashboard_news)):
    dashboard_news[i] = dashboard_news[i].replace(u'\xa0', u' ')
    print(dashboard_news[i])

for e, item in enumerate(dashboard_link):
    response2 = requests.get(item)
    path_list = html.fromstring(response2.text)
    dashboard_date2 = path_list.xpath('''//span[@class='mg-card-source__time']/@datetime''')

list_news3 = []

for t, i in enumerate(dashboard_news):
# создание словарей для добавления
    list_news3.append({"news_name": dashboard_news[t], "source": source2[t], "link": dashboard_link[t], "date": dashboard_date[t]})
#добавление в БД
news_db.insert_many(list_news3)
