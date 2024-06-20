import scrapy
import json
from mercadolibre_scraper.items import Product


class MercadolibreSpider(scrapy.Spider):
    name = "mercadolibre"
    start_urls = ["https://listado.mercadolibre.com.mx/coffee"]

    query = 'coffee'
    limit_per_query = 100
    country = 'mx'
    valid_countries = {
        'ar': 'https://listado.mercadolibre.com.ar/',
        'bo': 'https://listado.mercadolibre.com.bo/',
        'br': 'https://listado.mercadolibre.com.br/',
        'cl': 'https://listado.mercadolibre.cl/',
        'co': 'https://listado.mercadolibre.com.co/',
        'cr': 'https://listado.mercadolibre.com.cr/',
        'do': 'https://listado.mercadolibre.com.do/',
        'ec': 'https://listado.mercadolibre.com.ec/',
        'gt': 'https://listado.mercadolibre.com.gt/',
        'hn': 'https://listado.mercadolibre.com.hn/',
        'mx': 'https://listado.mercadolibre.com.mx/',
        'ni': 'https://listado.mercadolibre.com.ni/',
        'pa': 'https://listado.mercadolibre.com.pa/',
        'py': 'https://listado.mercadolibre.com.py/',
        'pe': 'https://listado.mercadolibre.com.pe/',
        'sv': 'https://listado.mercadolibre.com.sv/',
        'uy': 'https://listado.mercadolibre.com.uy/',
        've': 'https://listado.mercadolibre.com.ve/',
    }

    def parse(self, response):
        # The xpath not works for all the types of search results
        product_urls = response.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--title"]/a/@href').getall()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        script = response.xpath('//script[contains(text(), "window.__PRELOADED_STATE__")]/text()').get()
        data = script.split('window.__PRELOADED_STATE__ =')[1]
        data = data.split('};')[0] + '}'
        data = json.loads(data)
        sold_stock = data['initialState']['components']['track']['gtm_event'].get('soldStock', None)

        yield Product(
            id=data['initialState']['id'],
            name=data['initialState']['components']['header']['title'],
            price=data['initialState']['components']['price']['price']['value'],
            sold_stock=sold_stock,
            rating={
                'average': data['initialState']['components']['reviews_capability_v3']['rating']['average'],
                'amount': data['initialState']['components']['reviews_capability_v3']['rating']['amount'],
                'levels': data['initialState']['components']['reviews_capability_v3']['rating']['levels'],
            },
            reviews=data['initialState']['components']['reviews_capability_v3']['reviews'],
            seller=data['initialState']['components']['seller_experiment']['seller'],
            # gallery=data['initialState']['components']['gallery'],
        )

