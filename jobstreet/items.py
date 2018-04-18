# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	link = scrapy.Field()
	position = scrapy.Field()
	companyName = scrapy.Field()
	industry = scrapy.Field()
	address = scrapy.Field()
	companySize = scrapy.Field()
	publicTrans = scrapy.Field()
	jobDescription = scrapy.Field()
	postingDate = scrapy.Field()
	benefit = scrapy.Field()
	yearsExp = scrapy.Field()
