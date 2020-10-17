import scrapy
from scrapy.http import HtmlResponse
from leruaParser.items import LeruaItem
from scrapy.loader import ItemLoader  # создается для разгрузки программы  от extract, работает через items
# import Image

class ExampleSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):  # забирает параметр поиска из runner
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']  # благодаря свойствам объетка мы можем
        # определить с внешней стороны принимаемый параметр для поиска
        self.query = search
        self.recursion_depth = 1

    def parse(self, response: HtmlResponse):  # получение ссылок
        ads_links = response.xpath('''//a[@class = "plp-item__info__title"]''')
        for link in ads_links:  # переход по ссылкам спарсенным на странице
            yield response.follow(link, callback=self.parse_ads)

        try:
            next_page = response.xpath('''//a[@navy-arrow='next']/@href''').extract()[0]
            if next_page:
                self.recursion_depth += 1
                yield response.follow(next_page,callback=self.parse)
        except IndexError:
            print(f'Достигнута максимальная глубина в размере {self.recursion_depth} страниц')


    def parse_ads(self, response: HtmlResponse):  # сбор данных с каждой страницы
        loader = ItemLoader(item=LeruaItem(),
                            response=response)  # создается для разгрузки программы  от extract, работает через items
        loader.add_xpath('name', '''//h1/text()''')  # name для того, чтобы из пути извлекался текст и присваивался сразу в переменную items
        loader.add_xpath('price', '''//span[contains(@slot, "price")]/text()''')
        loader.add_xpath('photo','''//source[contains(@srcset, '2000')]/@data-origin''')
        loader.add_xpath('table_items','''//div[@class = 'def-list__group']//dd/text()''')
        loader.add_xpath('table_keys','''//div[@class = 'def-list__group']//dt/text()''')
        loader.add_value('url', response.url)
        yield loader.load_item()
