import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags, remove_tags_with_content

def read_church_websites():
	df = pd.read_csv('USA Church List Database ReferenceUSA RANDOM SAMPLE.csv')
	church_websites = df['Website']
	return church_websites

class ChurchSpider(scrapy.Spider):
	name = 'churchspider'
	church_websites = read_church_websites()

	# append https:// to all URLs
	start_urls = []
	for i, row in church_websites.iteritems():
		if "//" not in row:
			start_urls.append('http://' + row)

	def parse(self, response):
		# remove <script> tags from <p> elements
		for text in response.css('p'):
			yield {'text': remove_tags(remove_tags_with_content(text.extract(), ('script', )))}

		# add new URLs that are descendants of the request URL (same domain)
		for next_page in response.css('div > a'):
			a_tag = next_page.extract()
			if "href=" in a_tag:
				link = (a_tag.split('href="')[1]).split('"')[0]
				if link.count("/") > 2:
					if link.split("/")[2] in response.request.url:
						yield response.follow(next_page, self.parse)

