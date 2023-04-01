# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Movie(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    director = scrapy.Field()
    classification = scrapy.Field()
    rating = scrapy.Field()
    time = scrapy.Field()
    genres = scrapy.Field()
    pass
