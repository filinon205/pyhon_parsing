import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem # импорт структуры данных из items


class SuperjobRuSpider(scrapy.Spider):
    name = 'SjruSpider'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1']

    def parse(self, response:HtmlResponse): #response загружен в качестве дома

        vacansies = response.xpath('''//div[@class='jNMYr GPKTZ _1tH7S']//a/@href''').extract() # получаем все ссылки на вакансию
        for vacancy in vacansies:
            yield response.follow(vacancy, callback=self.vacancy_parse) # callback  ссылается на конечный метод в котором собирается основная информация по вакансиям (метод определим ниже vacancy_parse)

        next_page = response.xpath('''//span[contains(text(),'Дальше')]/../../../@href''').extract_first()  # выбор кнопки дальше по css селектору (ссылка)
        if next_page:  # и выбор именно первого элемента, если подтянутся похожие
            yield response.follow(next_page,callback=self.parse)  # запоминает где остановилась функция и при повторном вызове начинает с последней точки,
                # метод follow позволяет делать get запрос в рамках одной сессии callback возвращает рекурсивно обратно значение функции
                #  с переходом на новую страницу в response, функция зацикливается пока не переберт все значения next_page

    def vacancy_parse(self, response: HtmlResponse):

        name = response.css('h1 ::text').extract_first()
        salary = response.xpath('''//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()''').extract()
        link = response.url
        yield JobparserItem(name=name, salary = salary, link = link) #через yield создается объект JobparserItem  в атрибуты которого  переданы свойства vacancy_parse
        print()
