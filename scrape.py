import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags, remove_tags_with_content

def read_church_websites():
	df = pd.read_csv('USA Church List Database ReferenceUSA RANDOM SAMPLE.csv')
	church_websites = df['Website']
	return church_websites
	# print(church_websites)
	# print(church_websites.iloc[0])

class ChurchSpider(scrapy.Spider):
	name = 'churchspider'
	church_websites = read_church_websites()
	print(church_websites)

	start_urls = ['http://' + church_websites.iloc[0], 'http://' + church_websites.iloc[1]]
	print(start_urls)

	# rules = (
	# 	Rule(LinkExtractor(allow_domains=start_urls), callback='parse_item', follow=True),
	# )

	# def parse_item(self, response):
	# 	item = dict()
	# 	item['url'] = response.url
	# 	item['title'] = response.meta['link_text']
	# 	# extracting basic body
	# 	item['body'] = '\n'.join(response.xpath('//text()').extract())
	# 	# or better just save whole source
	# 	return item


	def parse(self, response):
		for text in response.css('p'):
				yield {'text': remove_tags(remove_tags_with_content(text.extract(), ('script', )))}

		for next_page in response.css('div > a'):
				a_tag = next_page.extract()
				link = (a_tag.split('href="')[1]).split('"')[0]
				if "/" in link:
					if link.split("/")[2] in response.request.url:
						yield response.follow(next_page, self.parse)


# if __name__ == "__main__":
	