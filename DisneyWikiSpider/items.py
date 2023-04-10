# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import TakeFirst, MapCompose

def to_int(value):
    try:
        return int(value)
    except ValueError:
        return None 

def to_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None 

def clean_revenue(revenue):
    revenue  = revenue.replace(',', '')
    m = re.search('\$\d+(\.\d+)*', revenue)
    if m is None:
        return None 
    value = float(m.group()[1:]) 
    if 'million' in revenue:
        value *= 10**6
    elif 'billion' in revenue:
        value *= 10**9
    return int(value)
      

class Movie(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    original_title = scrapy.Field(
        output_processor=TakeFirst()
    )
    director = scrapy.Field()
    parental_guide = scrapy.Field(
        output_processor=TakeFirst()
    )
    studio = scrapy.Field()
    imdb_rating = scrapy.Field(
        input_processor=MapCompose(to_float),
        output_processor=TakeFirst()
    )
    duration = scrapy.Field(
        input_processor=MapCompose(to_int),
        output_processor=TakeFirst()
    )
    gross_revenue = scrapy.Field(
        input_processor=MapCompose(clean_revenue),
        output_processor=TakeFirst()
    )
    year = scrapy.Field(
        output_processor=TakeFirst()
    )
    genres = scrapy.Field()
    cast = scrapy.Field()
    characters = scrapy.Field()
    awards = scrapy.Field()
    preceded_by = scrapy.Field(
        output_processor=TakeFirst()
    )
