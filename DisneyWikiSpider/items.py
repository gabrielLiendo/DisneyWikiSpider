# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import TakeFirst, MapCompose

    
def filter_original_title(title):
    return title.removeprefix('Título original: ')

def filter_minutes(time):
    m = re.search('[0-9]+', time)
    return m.group()

class Movie(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    original_title = scrapy.Field(
        input_processor=MapCompose(filter_original_title),
        output_processor=TakeFirst()
    )
    director = scrapy.Field()
    parental_guide = scrapy.Field(
        output_processor=TakeFirst()
    )
    imdb_rating = scrapy.Field(
        output_processor=TakeFirst()
    )
    duration = scrapy.Field(
        input_processor=MapCompose(filter_minutes),
        output_processor=TakeFirst()
    )
    genres = scrapy.Field()
