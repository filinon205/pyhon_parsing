# связка настроек с пауком для его запуска. Программа для контроля запуска паука

from scrapy.crawler import CrawlerProcess  # Модуль отвечающий за процесс сбора данных
from scrapy.settings import Settings

from leruaParser import settings  # подключаем проект и подтягиваем его настройки
from leruaParser.spiders.lerua import ExampleSpider  # импортируем класс с пауком
#from avitoparser.spiders.avitoru import ExampleSpider # подключение второго паука

if __name__ == '__main__':  # заглушка для проверки на самостоятельный запуск или на запуск из другого проекта
    crawler_settings = Settings()  # создаём экземпляр класса пустой без доп. настроек
    crawler_settings.setmodule(settings)  # забирает в себя настройки и преобразует в словарь
    process = CrawlerProcess(settings=crawler_settings)  # процесс содержит настройки которые передали, не больше
    process.crawl(ExampleSpider, search='смесители')  # Указываем какой паук будет работать внутри процесса,
                                                                # указываем критерий поиска в search, который передастся в параметр url паука (внутри конструктора)
    #process.crawl(SuperjobRuSpider) # указываем например еще одного паука в рамках одного процесса

    process.start()  # запуск скраппера. При вызове создастся класс  HhruSpider, отработает get запрос (ответ падает в аргумент метода класса response)
                     # и вызовутся методы внутри класса (скрипт lerua)
