from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# настройка сервера MongoDB
client = MongoClient('localhost', 27017)
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe',
                          options=chrome_options)  # создаем драйвер для полдключения к нашему драйверу. Объект в который все будет загружаться



# mail -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Подключение к БД
# db = client['почта_mail']
# # Указатель на коллекцию
# mail_DB = db.test_collection
# mail_db = db.mail_DB

# driver.get(
#     "https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%2F&allow_external=1&from=octavius")
# time.sleep(1)
# login = driver.find_element_by_xpath('''//input[@placeholder='Имя аккаунта']''')  # поиск по классу у объекта driver
# time.sleep(0.1)
# login.send_keys('study.ai_172@mail.ru')  # заполнение формы логина
# login.send_keys(Keys.RETURN) # нажимаем кнопку для входа
# time.sleep(1)
# password = driver.find_element_by_xpath('''//input[@placeholder='Пароль']''')
# password.send_keys('NextPassword172')
# time.sleep(0.5)
# password.send_keys(Keys.RETURN)
# time.sleep(3)
# authors = []
# date = []
# SCROLL_PAUSE_TIME = 0.5


# dashboard = driver.find_element_by_xpath(r'''//div[@class='scrollable g-scrollable scrollable_bright scrollable_footer']//div[@class='scrollable__container']''') # выбираем всю доску с письмами
# mails_link1 = []
# mails_link2 = []
# authors = []
# date = []
# tema_ = []
# text = []
# # прокрутка вниз до элемента
# for i in range(4):
#     driver.implicitly_wait(2)
#     # выбираем все письма
#     mails = driver.find_elements_by_xpath('''//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']''')
#
#     for mail in mails: # собираем список ссылок
#         link = mail.get_attribute('href')
#         mails_link1.append(link)
#
#     actions = ActionChains(driver)
#     actions.move_to_element(mails[-1])
#     actions.perform()
# # убираем дубли ссылок
# mails_link2 = list(set(mails_link1))
# for x in mails_link2:  # перебираем информацию по каждому письму
#     driver.get(x)
#     time.sleep(2)
#     #link = driver.get(x.get_attribute('href'))
#     authors.append(driver.find_element_by_xpath('''//div[@class='letter__author']''').text)
#     date.append(driver.find_element_by_class_name('letter__date').text)
#     time.sleep(1)
#     tema_.append(driver.find_element_by_xpath('''//h2[@class='thread__subject']''').text)
#     time.sleep(1)
#     text.append(driver.find_element_by_class_name('letter__body').text)
#
# mail_hgc = []
# for t, i in enumerate(mails):
# # создание словарей для добавления
#     mail_hgc.append({"mail_theme": tema_[t], "date": date[t], "author": authors[t], "text": text[t]})
# #добавление в БД
# mail_db.insert_many(mail_hgc)

# МВидео----------------------------------------------------------------------------------------------------
url = 'https://www.mvideo.ru'
driver.get(url)

# Подключение к БД
db = client['хиты_продаж_mvideo']
# Указатель на коллекцию
mvideo_DB = db.test_collection
mvideo_db = db.mvideo_DB

spisok = driver.find_element_by_xpath(
        '//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]')
# прокрутка вниз до списка хитов
driver.implicitly_wait(2)
actions = ActionChains(driver)
actions.move_to_element(spisok)
actions.perform()

good_name = []
good_price = []
links = []
while True:
    try:
        button = WebDriverWait(spisok, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]'))
        )
        goods = spisok.find_elements_by_css_selector('li.gallery-list-item')
        for good in goods:
            name = good.find_element_by_tag_name('h4').text
            price = good.find_element_by_class_name('c-pdp-price__current').text
            price = price.replace('¤', '')
            link = good.find_element_by_class_name('sel-product-tile-title').get_attribute('href')
            if name == "" or price == "" or link == "":
                continue
            good_name.append(name)
            good_price.append(price)
            links.append(link)
        button.click()
    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

goods_mvideo= []
for t, i in enumerate(good_name):
# создание словарей для добавления
    goods_mvideo.append({"Наименование товара": good_name[t], "Цена": good_price[t], "Ссылка": links[t]})
#добавление в БД
mvideo_db.insert_many(goods_mvideo)
