import scrapy
import json
from mercadolibre_scraper.items import Product


class MercadolibreSpider(scrapy.Spider):
    name = "mercadolibre"
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

    def __init__(self, query, country, *args, **kwargs):
        super(MercadolibreSpider, self).__init__(*args, **kwargs)
        if country.lower() not in self.valid_countries:
            raise ValueError(f"Country '{country}' not supported, please use one of {', '.join(self.valid_countries.keys())}")
        if not query:
            raise ValueError("Query is required")
        query_formatted = query.replace(' ', '-')
        domain = self.valid_countries[country]
        self.start_urls = [f'{domain}{query_formatted}']

    def parse(self, response):
        # The xpath not works for all the types of search results
        product_urls = response.xpath('//li[contains(@class, "ui-search-layout__item")]//div[@class="ui-search-item__group ui-search-item__group--title"]/a/@href').getall()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        script = response.xpath('//script[contains(text(), "window.__PRELOADED_STATE__")]/text()').get()
        data = script.split('window.__PRELOADED_STATE__ =')[1]
        data = data.split('};')[0] + '}'
        data = json.loads(data)

        sold_stock = data['initialState']['components']['track']['gtm_event'].get('soldStock', None)
        if data['initialState']['components'].get('reviews_capability_v3'):
            reviews = data['initialState']['components']['reviews_capability_v3'].get('reviews', [])
        else:
            reviews = []
        if data['initialState']['components'].get('reviews_capability_v3')\
                and data['initialState']['components']['reviews_capability_v3'].get('rating'):
            rating = {
                'average': data['initialState']['components']['reviews_capability_v3']['rating']['average'],
                'amount': data['initialState']['components']['reviews_capability_v3']['rating']['amount'],
                'levels': data['initialState']['components']['reviews_capability_v3']['rating']['levels'],
            }
        else:
            rating = None

        yield Product(
            url=response.url,
            id=data['initialState']['id'],
            name=data['initialState']['components']['header']['title'],
            price=data['initialState']['components']['price']['price']['value'],
            sold_stock=sold_stock,
            rating=rating,
            reviews=reviews,
            seller=data['initialState']['components']['seller_experiment']['seller'],
            # gallery=data['initialState']['components']['gallery'],
        )


