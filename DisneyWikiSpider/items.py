# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import TakeFirst, MapCompose

    
def filter_original_title(title):
    return title.removeprefix('Título original: ')

def filter_rating(rating):
    try:
        return float(rating.replace(',', '.'))
    except ValueError:
        return None 
    
def filter_minutes(time):
    m = re.search('[0-9]+', time)
    return int(m.group())

def filter_year(release_date):
    m = re.search('\d{4}', release_date)
    if m is None:
        return None
    else:
        return int(m.group())

def filter_revenue(revenue):
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
        input_processor=MapCompose(filter_original_title),
        output_processor=TakeFirst()
    )
    director = scrapy.Field()
    parental_guide = scrapy.Field(
        output_processor=TakeFirst()
    )
    studio = scrapy.Field()
    imdb_rating = scrapy.Field(
        input_processor=MapCompose(filter_rating),
        output_processor=TakeFirst()
    )
    duration = scrapy.Field(
        input_processor=MapCompose(filter_minutes),
        output_processor=TakeFirst()
    )
    gross_revenue = scrapy.Field(
        input_processor=MapCompose(filter_revenue),
        output_processor=TakeFirst()
    )
    year = scrapy.Field(
        input_processor=MapCompose(filter_year),
        output_processor=TakeFirst()
    )
    genres = scrapy.Field()
    cast = scrapy.Field()
