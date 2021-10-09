  
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
        '''Obtener la lista de pag'''
        list_pages = []
        listaDePaginas = []
        for i in range(1, 30):
            list_pages.append('https://empleosti.com.mx/empleos??page=' + str(i))

        '''
        for pages in list_pages:
            response.xpath('//ul[@class="job-eti"]//li/a/@href').getall()
        '''  
        
        listaDePaginas = response.xpath('//ul[@class="job-eti"]//li/a/@href').getall()
        
        for link in listaDePaginas:
            yield response.follow(link, callback=self.parse_pages)
      
    def parse_pages(self, response):
        titles = response.xpath('//h1[@class="section-title"]/text()').get()
        salary = response.xpath('//*[@id="vacancy-content"]/ul/li[1]/p[@class="gray-subarea-title"]/text()').get()
        place = response.xpath('//*[@id="vacancy-content"]/ul/li[2]/p[@class="gray-subarea-title"]/a/text()').get()
        type = response.xpath('//*[@id="vacancy-content"]/ul/li[3]/p[@class="gray-subarea-title"]/text()').get()
        english = response.xpath('//*[@id="vacancy-content"]/ul/li[4]/p[@class="gray-subarea-title"]/text()').get()
        company = response.xpath('//*[@id="searchable-enterprise"]/text()').get()
        description =  response.xpath('//*[@id="vacancy-description"]').get()
        
        yield {
            'titulo': titles,
            'salario': salary,
            'lugar': place,
            'tipo_trabajo': type,
            'nivel_ingles': english,
            'empresa' : company,
            'descripcion' : description,
        }