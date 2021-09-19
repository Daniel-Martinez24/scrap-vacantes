  
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://myanimelist.net/anime/genre/24/Sci-Fi'
    ]

    custom_settings = {
        'FEED_URI': 'results/scifianimes.cvs',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True
    }

    def parse(self, response):
        
        listaDePaginas = response.xpath('//div[@class="pagination ac"]/a/@href').getall()
        
        for link in listaDePaginas:
            yield response.follow(link, callback=self.parse_pages)
      
    def parse_pages(self, response):
        scores = response.xpath('//span[@title="Score"]/text()').getall()
        dates = response.xpath('//span[@class="remain-time"]/text()').getall()
        titles = response.xpath('//a[@class="link-title"]/text()').getall()
        
        scores = [score.strip() for score in scores ]
        dates = [date.strip() for date in dates]
        
        for posicion in range(len(scores)):
            yield {
                'titulo ': titles[posicion],
                'score': scores[posicion],
                'date': dates[posicion]
            }