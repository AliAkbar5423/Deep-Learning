import scrapy

class newsMelek(scrapy.Spider):
    name = 'melekpolitik.com'
    start_urls = ['https://medanseru.info/category/korupsi/',
                  'https://medanseru.info/category/politik/',
                  'https://medanseru.info/category/nasional/',
                  'https://medanseru.info/category/internasional/',
                  'https://medanseru.info/category/artis/',
                  'https://medanseru.info/category/kriminal/',
                  ]

    def parse(self, response):
        for medan in response.css('div.td_module_11.td_module_wrap.td-animation-stack'):
            item = {
                'judul': medan.css('div.item-details > h3.entry-title.td-module-title > a::text').extract_first(),
                'deskripsi': medan.css('div.td-excerpt::text').extract_first(),
            }
            yield item

            #pagination
            next_page = response.css('div.page-nav.td-pb-padding-side > a::attr(href)').extract()[-1]
            if next_page is not None:
                yield response.follow(url = next_page, callback = self.parse)
