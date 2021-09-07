# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoothItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Href = scrapy.Field()
    Name = scrapy.Field()
    InfoStr = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Country = scrapy.Field()
    Zip = scrapy.Field()
    Phone = scrapy.Field()
    Website = scrapy.Field()
    Booths = scrapy.Field()
    About = scrapy.Field()
    ProductCategories = scrapy.Field()