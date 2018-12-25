import scrapy


class MultipleQuotesSpider(scrapy.Spider):
    name = "multiple-quotes"
    allowed_domains = ["panjimas.com"]
    start_urls = ['http://www.panjimas.com/category/news/']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for panjimas in response.css('div.post-content'):
            item = {
                'judul': panjimas.css('a::text').extract_first(),
                'deskripsi': panjimas.css('p::text').extract_first(),
            }
            yield item

            #pagination
            next_page = response.css('div.navigation > a::attr(href)').extract()[-1]
            if next_page:
                next_page = response.urljoin(next_page)
                yield response.follow(url = next_page, callback = self.parse, dont_filter = True)
			
			
