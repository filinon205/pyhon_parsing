import scrapy
from scrapy.http import HtmlResponse # загружаем для указания к какому типу относится объект response, чтобы просмотреть методы выбранного типа ЧЕРЕЗ .
from jobparser.items import JobparserItem # импорт структуры данных из items

class HhruSpider(scrapy.Spider):
    name = 'hhru' #  имя паука
    allowed_domains = ['hh.ru'] # домен в котором будет работать паук, можно работать сразу с 2-мя сайтами одновременно
    start_urls = ['https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response:HtmlResponse): #response загружен в качестве дома

        vacansies = response.css('div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract() # получаем все ссылки на вакансию
        for vacancy in vacansies:
            yield response.follow(vacancy, callback=self.vacancy_parse) # callback  ссылается на конечный метод в котором собирается основная информация по вакансиям (метод определим ниже vacancy_parse)

        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()  # выбор кнопки дальше по css селектору (ссылка)
        if next_page:  # и выбор именно первого элемента, если подтянутся похожие
            yield response.follow(next_page,callback=self.parse)  # запоминает где остановилась функция и при повторном вызове начинает с последней точки,
                # метод follow позволяет делать get запрос в рамках одной сессии callback возвращает рекурсивно обратно значение функции
                #  с переходом на новую страницу в response, функция зацикливается пока не переберт все значения next_page

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        link = response.url
        yield JobparserItem(name=name, salary = salary, link = link) #через yield создается объект JobparserItem  в атрибуты которого  переданы свойства vacancy_parse
        print()
