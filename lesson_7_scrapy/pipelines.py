# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# для работы с картинками необходимо установить pip install pillow

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline  # подключение класса для обработки картинок (ссылок)
import scrapy
from pymongo import MongoClient
import os
from urllib.parse import urlparse


class LeruaParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua_DB
    def process_item(self, item, spider):
        item['table'] = dict(zip(item['table_keys'],item['table_items']))
        item['query'] = spider.query

        del item['table_keys'], item['table_items']
        collection = self.mongo_base[spider.name]

        db_query_par = {'url':item['url'], 'name': item['name']}
        if collection.count_documents(db_query_par) > 0:
            old_query = [x['query'] for x in collection.find(db_query_par)]
            if item['query'] not in old_query:
                old_query.append(item['query'])
            collection.update_one(db_query_par,
                                    {
                                        '$set': {
                                            'price': item['price'],
                                            'table': item['table'],
                                            'photo': item['photo'],
                                            'query': old_query
                                        }
                                    }
                                    )
        else:
            collection.insert_one(item)
        return item

class LeruaPhotosPipeline(ImagesPipeline):  # создаем класс для обработки фоток, наследуем свойства подгруженного класса для работы с картинками
    def get_media_requests(self, item, info):  # метод класса для скачки фоток
        if item['photo']:  # проверка на наличие фотографии
            for img in item['photo']:  # пробегаемся по каждой фотке
                try:
                    yield scrapy.Request(img)  # get запрос на указанную ссылку
                except Exception as e:  # вызов ошибки при арушении процдуры скачки картинки
                    print(e)

    def file_path(self, request, response=None, info=None):
        return 'files/' + info.spider.query + '/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):  # метод необходимый для сортировки фоток при скачке
        if results:  # проверка были ли фотки вообще?
            item['photo'] = [itm[1] for itm in results if itm[0]]  # перезапись ссылок фото на более информативную структуру словаря метода item_completed

        return item  # передача данных дальше по конвееру