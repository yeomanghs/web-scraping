# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from FCA.items import FcaItem
import re

class FCA(scrapy.Spider):
    name = "fca"
    start_urls = ["https://www.bnm.gov.my/financial-consumer-alert-list"]

    def parse(self, response):
        info = FcaItem()
        nameList = response.xpath('//td[1]/text()').extract()
        websiteList = response.xpath('//td[2]/text()').extract()
        dateList = response.xpath('//td[3]/text()').extract()
        # print(content)
        for no, name in enumerate(nameList):
            info['Name'] = re.sub("\xa0", '', name)
            info['Website'] = re.sub("\xa0", '', websiteList[no])
            info['Date'] = re.sub("\xa0", '', dateList[no])
            yield info