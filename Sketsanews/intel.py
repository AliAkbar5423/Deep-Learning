import scrapy

class newsIntel(scrapy.Spider):
    name = 'sketsanews.com'
    start_urls = ['https://sketsanews.com/news/']

    def parse(self, response):
        for sketsa in response.css('article'):
            item = {
                'judul': sketsa.css('header.entry-header > h1.entry-title > a::text').extract_first(),
                'deskripsi': sketsa.css('div.excerpt.col-sm-8.col-xs-6.hide300px > p::text').extract_first(),
            }
            yield item

            #pagination

            next_page = response.css('ul.pagination.pagination-sm > li > a::attr(href)').extract()[-2]
            if next_page is not None:
               yield response.follow(url = next_page, callback = self.parse)
            
