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
            
        next_list = response.xpath('//a[contains(@class, "category-page__pagination-next")]/@href').get()
        if next_list is not None:
            yield scrapy.Request(next_list, callback=self.parse)
            
    def parse_movie(self, response):        
        l = ItemLoader(Movie(), response)

        l.add_xpath('director', '//div[@data-source="director"]/div/descendant::text()', re='^\w+[ +\w+]*$')
        l.add_xpath('studio', '//div[@data-source="studio"]/div/descendant::text()', re='^\w+[ +\w+]*$')
        l.add_xpath('year', '//div[@data-source="release"]/div/descendant::text()', re='\d{4}')
        l.add_xpath('duration', '//div[@data-source="time"]/div/text()', re='\d+')
        l.add_xpath('gross_revenue', '//div[@data-source="gross"]/div/text()')
        
        #Redirect to IMDB
        imdb_link = response.xpath('//td[@data-source="imdb_id"]/span/a/@href').get()
        
        if imdb_link is not None:
            yield scrapy.Request(imdb_link, callback=self.parse_imdb, meta={'movie': l.load_item()})
        else:   
            l.add_xpath('title', '//h2[@data-source="name"]/descendant::text()')
            l.add_xpath('original_title', '//h2[@data-source="name"]/descendant::text()')
            yield l.load_item()
        
    def parse_imdb(self, response):
        l = ItemLoader(response.meta['movie'], response)

        #Search again for title, year and director
        l.add_xpath('title', '//h1[@data-testid="hero__pageTitle"]/span/text()')
        l.add_xpath('year', '//a[contains(@href, "/releaseinfo")]/text()', re='\d{4}')
        l.add_xpath('director', '//div[@data-testid="genres"]/following-sibling::div/div/ul/li[1]/div/ul/li/a/text()', re='^\w+[ +\w+]*$')
        
        l.add_xpath('original_title', '//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()', re='Título original: (.*)')
        l.add_xpath('parental_guide', '//a[contains(@href, "/parentalguide")]/text()')
        l.add_xpath('imdb_rating','//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]/text()')
        l.add_xpath('genres', '//div[@data-testid="genres"]/div[2]/a/span/text()')
        l.add_xpath('cast', '//a[@data-testid="title-cast-item__actor"]/text()')
        l.add_xpath('characters', '//a[@data-testid="cast-item-characters-link"]/span/text()', re='^\w+[ +\w+]*$')
        
        awards_link = response.xpath('//li[@data-testid="award_information"]/a/@href').get()
        
        if awards_link is not None:
            yield response.follow(awards_link, callback=self.parse_awards, meta={'movie': l.load_item()})
        else:        
            yield l.load_item()
    
    def parse_awards(self, response):
        # Parse awards list
        award_list = response.xpath('//td[contains(@class,"title_award_outcome")]')
        awards = [self.clean_award(award) for award in award_list]
        
        # Load list into Item
        l = ItemLoader(response.meta['movie'], response)         
        l.add_value('awards', awards)
        
        yield l.load_item()
        
    def clean_award(self, award):
        outcomes = {'Winner': 1, 'Nominee': 0}
        
        name = award.xpath('.//span/text()').get()
        result = award.xpath('.//b/text()').get()
        
        return {'name': name, 'winner': outcomes[result]}