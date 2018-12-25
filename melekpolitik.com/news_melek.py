import scrapy

class newsMelek(scrapy.Spider):
    name = 'melekpolitik.com'
    start_urls = ['http://www.melekpolitik.com/category/berita/',
                  'http://www.melekpolitik.com/category/artikel/',
                  'http://www.melekpolitik.com/category/opini/',
                  ]

    def parse(self, response):
        for melek in response.css('div.jeg_postblock_content'):
            item = {
                'judul': melek.css('h3.jeg_post_title > a::text').extract_first(),
                'deskripsi': melek.css('div.jeg_post_excerpt > p::text').extract_first(),
            }
            yield item

            #pagination
            next_page = response.css('div.jeg_navigation.jeg_pagination.jeg_pagenav_1.jeg_aligncenter.no_navtext.no_pageinfo > a:last-child::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(url = next_page, callback = self.parse)
            
