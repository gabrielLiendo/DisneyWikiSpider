import scrapy

class MovieSpider(scrapy.Spider):
    name = 'moviespider'
    start_urls = ['https://disney.fandom.com/wiki/Category:Films?from=Bad+Hair+Day+%28film%29']

    def parse(self, response):
        movie_links = response.css('.category-page__member-link::attr(href)').getall()
        for link in movie_links:
            if "Category:" in link:
                continue
            yield scrapy.Request('https://disney.fandom.com' + link, callback=self.parse_movie)
            
    def parse_movie(self, response):
        #Check for infobox
        aside = response.css('.portable-infobox')
        if aside is None:
            return
        
        #Construct Movie JSON
        movie = {}
        
        #Title
        movie['title'] = aside.css('h2[data-source="name"] *::text').get()

        #Director
        movie['director'] = aside.xpath('.//div[@data-source="director"]/div/descendant::text()').get()
        
        #Duration
        time = aside.css('div[data-source="time"] div::text').re_first('[0-9]+')
        if time:  
            movie['time'] = time
            
        #IMDB
        imdb_link = aside.css('td[data-source="imdb_id"] a::attr(href)').get()
        
        if(imdb_link is not None):
            yield scrapy.Request(imdb_link, callback=self.parse_imdb, meta={'movie': movie})
        else: 
            yield movie
        
    def parse_imdb(self, response):
        movie = response.meta['movie']
        
        #Data in header
        header = response.xpath('//h1[@data-testid="hero__pageTitle"]')

        movie['title'] = header.xpath('.//span/text()').get()
        original_title = header.xpath('.//following-sibling::div/text()').get()
        if original_title is None:
            movie['original_title'] = movie['title']
        else:
            movie['original_title'] = original_title.removeprefix('Título original: ')
        
        classification = response.xpath('//h1[@data-testid="hero__pageTitle"]/following-sibling::ul/li/a[contains(@href, "/parentalguide")]/text()').get()
        if classification is not None:
            movie['classification'] = classification
        
        movie['rating'] = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]/text()').get()
        movie['genres'] = response.xpath('//div[@data-testid="genres"]/div[2]/a/span/text()').getall()
        
        yield movie