# Define your item pipelines here # финальная обработка данных, где все данные собираются в структуру
# после обработки в JobparserItemb из items. json упадет в переменную item
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# обработка данных здесь
# все доп. поля указывать в JobparserItem, иначе в словаре новые поля работать не будут

from pymongo import MongoClient # подключение mongodb

class JobparserPipeline: # данные собираются в форме словаря

    def __init__(self): # внедрение подключения к mongodb
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancyHH

        # обработка данных зп

    def process_item(self, item, spider):
        salary = item['salary']
        vacancy_name = ''.join(item['name'])
        link = item['link']
        if spider.name == 'hhru': # условия обработки для паука hh
            if salary[0] == 'з/п не указана':
                min_salary = None
                max_salary = None
                curency = None
            else:
                if salary[0] == ' до ':
                    max_salary = salary[1].replace(r'\xa', '')
                    min_salary = None
                elif salary[0] == 'от ' and len(salary)<6:
                    min_salary = salary[1].replace(r'\xa', '')
                    max_salary = None
                else:
                    min_salary = salary[1].replace(r'\xa', '')
                    max_salary = salary[3].replace(r'\xa', '')

        if spider.name == 'SjruSpider': # условия обработки для паука sj
            if salary[0] == 'з/п не указана' or salary[0] == 'По договорённости':
                min_salary = None
                max_salary = None
            elif salary[0] == 'до':
                max_salary = salary[2].replace(r'\xa', '')
                min_salary = None
            elif salary[0] == 'от' and len(salary)==4:
                max_salary = None
                min_salary = salary[2].replace(r'\xa0руб.','')
                min_salary = min_salary.replace(r'\xa','')
            elif len(salary) == 4 and salary[-1] == 'руб.':
                min_salary = salary[0].replace(r'\xa', '')
                max_salary = salary[1].replace(r'\xa0', '')
            elif len(salary) == 3 and salary[-1] == 'руб.':
                min_salary = salary[0].replace(r'\xa', '')
            else:
                print()

        vacancy_json = {
            'vacancy_name': vacancy_name, 'min_salary':min_salary,'max_salary':max_salary, 'link':link
        }

        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_json)
        print()
        return vacancy_json

