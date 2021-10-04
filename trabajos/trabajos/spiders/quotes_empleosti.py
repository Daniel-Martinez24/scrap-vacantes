  
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes_empleosti'
    start_urls = [
        'https://empleosti.com.mx/empleos?k='
    ]

    custom_settings = {
        'FEED_URI': 'results/empleos_ti.cvs',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True
    }

    def parse(self, response):
        
        listaDePaginas = response.xpath('//ul[@class="job-eti"]//li/a/@href').getall()
        
        for link in listaDePaginas:
            yield response.follow(link, callback=self.parse_pages)
      
    def parse_pages(self, response):
        titles = response.xpath('//h1[@class="section-title"]/text()').getall()
        salary = response.xpath('//*[@id="vacancy-content"]/ul/li[1]/p[@class="gray-subarea-title"]/text()').getall()
        place = response.xpath('//*[@id="vacancy-content"]/ul/li[2]/p[@class="gray-subarea-title"]/text()').getall()
        type = response.xpath('//*[@id="vacancy-content"]/ul/li[3]/p[@class="gray-subarea-title"]/text()').getall()
        english = response.xpath('//*[@id="vacancy-content"]/ul/li[4]/p[@class="gray-subarea-title"]/text()').getall()
        

        # scores = [score.strip() for score in scores ]
        # dates = [date.strip() for date in dates]
        
        for posicion in range(len(english)):
            yield {
                'titulo': titles[posicion],
                'salario': salary[posicion],
                'lugar': place[posicion],
                'tipo_trabajo': type[posicion],
                'nivel_ingles': english[posicion]
                # 'score': scores[posicion],
                # 'date': dates[posicion]
            }