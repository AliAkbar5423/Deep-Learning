import scrapy

class newsIyaa(scrapy.Spider):
	name = 'media.iyaa.com'

	def start_request(self):
		urls =   ['https://media.iyaa.com/post/category/tv-update/',
				  'https://media.iyaa.com/post/category/kabarartis/',
				  'https://media.iyaa.com/post/category/sinopsis/',
				  'https://media.iyaa.com/post/category/fashion/',
				  'https://media.iyaa.com/post/category/beauty/',
				  ]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for iyaa in response.css('article.evo-post'):
			item = {
				'judul': iyaa.css('div.evo-post-body > div.evo-post-inner > h3.evo-entry-title > a::text').extract_first(),
				'deskripsi':  iyaa.css('div.evo-post-body > div.evo-post-inner > div.evo-entry-content > p::text').extract_first(),
			}
			yield item

			#pagination
			next_page = response.css('div.nav-links > a::attr(href)').extract()[-1]
			if next_page is not None:
				yield response.follow(url = next_page, callback = self.parse)
			
