# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    sold_stock = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    seller = scrapy.Field()
    # gallery = scrapy.Field()

