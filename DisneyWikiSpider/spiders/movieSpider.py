import scrapy
from scrapy.loader import ItemLoader
from ..items import Movie

class MovieSpider(scrapy.Spider):
    name = 'moviespider'
    start_urls = ['https://disney.fandom.com/wiki/Category:Films']

    def parse(self, response):
        movie_links = response.css('.category-page__member-link::attr(href)').getall()
        for link in movie_links:
            if "Category:" in link:
                continue
            yield scrapy.Request('https://disney.fandom.com' + link, callback=self.parse_movie)
            
    def parse_movie(self, response):        
        l = ItemLoader(Movie(), response)

        l.add_xpath('director', '//div[@data-source="director"]/div/descendant::text()')
        l.add_xpath('studio', '//div[@data-source="studio"]/div/descendant::text()')
        l.add_xpath('year', '//div[@data-source="release"]/div/descendant::text()')
        l.add_xpath('duration', '//div[@data-source="time"]/div/text()')
        
        #Redirect to IMDB
        imdb_link = response.xpath('//td[@data-source="imdb_id"]/span/a/@href').get()
        
        if imdb_link is not None:
            yield scrapy.Request(imdb_link, callback=self.parse_imdb, meta={'movie': l.load_item()})
        else:   
            l.add_xpath('title', '//h2[@data-source="name"]/descendant::text()')
            yield l.load_item()
        
    def parse_imdb(self, response):
        l = ItemLoader(response.meta['movie'], response)

        l.add_xpath('title', '//h1[@data-testid="hero__pageTitle"]/span/text()')
        l.add_xpath('original_title', '//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()')
        l.add_xpath('parental_guide', '//a[contains(@href, "/parentalguide")]/text()')
        l.add_xpath('imdb_rating','//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]/text()')
        l.add_xpath('genres', '//div[@data-testid="genres"]/div[2]/a/span/text()')
        
        yield l.load_item()