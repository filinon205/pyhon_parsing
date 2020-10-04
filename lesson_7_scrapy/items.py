# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,  TakeFirst # обработчик спарсенных данных в items через loader. Обработчик применятеся к созданным полям
                                                            # таким образом обработчик создается сразу с переменной

def price_to_int(price):
    if price:
        return int(price.replace(' ',''))
    return price
def clear_strings(x):
    if x:
        return x.replace('/n','').rstrip().lstrip()
    return x

def replace(x):
    if x:
        return x.replace('.',' ')
    return x
class LeruaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst()) # все данные которые сюда залетят будут подвергнуты обработке. Данные обработуются только после того как накопятся до yield
    price = scrapy.Field(input_processor = MapCompose(price_to_int)) # input_processor данные обработаются сразу без накопления до yield
                                                                                # MapCompose(price_to_int) применяет к каждому полученному парсером элементу списка функцию
    photo = scrapy.Field()
    _id = scrapy.Field()
    table_items = scrapy.Field(input_processor=MapCompose(clear_strings))
    table_keys = scrapy.Field(input_processor=MapCompose(clear_strings,replace))
    url = scrapy.Field(output_processor=TakeFirst())
    query = scrapy.Field()
    table = scrapy.Field()