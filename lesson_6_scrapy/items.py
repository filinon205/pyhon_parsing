# Define here the models for your scraped items / описываем здесь свою структуру данных (по сути как таблицу) для собранных данных
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item): # класс нужно подключить к пауку
    # define the fields for your item here like:
    name = scrapy.Field() # по сути поле таблицы, данные тянутся из паука в данном случае из hhru
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    curency = scrapy.Field()
    _id = scrapy.Field()
    link = scrapy.Field()
    pass
