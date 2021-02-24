import scrapy

from scrapy.loader import ItemLoader
from ..items import CkbmeItem
from itemloaders.processors import TakeFirst


class CkbmeSpider(scrapy.Spider):
	name = 'ckbme'
	start_urls = ['https://www.ckb.me/opste/novosti']

	def parse(self, response):
		post_links = response.xpath('//a[@class="news-box-more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pagin-button next "]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="news-box__text-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="news-box-date"]/text()').get()

		item = ItemLoader(item=CkbmeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
