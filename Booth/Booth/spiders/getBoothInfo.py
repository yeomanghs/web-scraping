import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
#check folder name
from Booth.items import BoothItem
import pandas as pd
from scrapy import Selector
import re
import time
from selenium import webdriver
import chromedriver_binary

class BursaSpider(Spider):
    name = "boothInfo"
    start_urls = ['https://spi21.mapyourshow.com/8_0/explore/exhibitor-alphalist.cfm#/']

    def __init__(self):
        url = 'https://spi21.mapyourshow.com/8_0/explore/exhibitor-alphalist.cfm#/'
        self.filename = 'C:/Users/JiunShyanGoh/Documents/Upwork/DataScraping/Data/HrefList.csv'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')  

    #get hreflist using selenium    
    def getHrefList(self):
        hrefList = []
        with open(self.filename, 'r') as filehandle:
            for line in filehandle:
                hrefList.append(re.sub('\n','',line))
        return hrefList

    #test scraping in terminal: scrapy shell <website> to check if the webpage is dynamic
    def parse(self,response):
        uniqueHrefList = self.getHrefList()
        
        for href in uniqueHrefList:
            boothInfo = BoothItem()
            boothInfo['Href'] = href
            request = scrapy.Request(href, callback = self.parseDetails)
            request.meta['boothInfo'] = boothInfo
            yield request

    def parseDetails(self, response):
        boothInfo = response.meta['boothInfo']
        name = response.xpath("//h1/text()").extract()[0]
        boothInfo['Name'] = name

        allInfoList = response.xpath("//div[@class = 'wrapper-centered']/node()").extract()
        allInfoList2 = [re.sub("\<.*?\>", '', i) for i in allInfoList]
        allInfoList2 = [re.sub("\r|\n|\t", '', i) for i in allInfoList2]
        infoStr = '\n'.join([i for i in allInfoList2 if i!=''])
        boothInfo['InfoStr'] = infoStr
        for col in ['Address', 'City', 'State', 'Zip']:
            if re.search("%s:\n(.*?)\n"%col, infoStr):
                boothInfo[col] = re.search("%s:\n(.*?)\n"%col, infoStr).group(1)
            else:
                boothInfo[col] = ''

        for col in ['Country', 'Phone', 'Website']:
            if re.search("%s:(.*?)\n"%col, infoStr):
                boothInfo[col] = re.search("%s:(.*?)\n"%col, infoStr).group(1)
            else:
                boothInfo[col] = ''

        for col in ['Booths']:
            if re.search("%s(.*?)\n"%col, infoStr):
                boothInfo[col] = re.search("%s(.*?)\n"%col, infoStr).group(1)
            else:
                boothInfo[col] = ''

        for col in ['About']:
            if re.search("%s %s\n(.*?)\n"%(col,name), infoStr):
                boothInfo[col] = re.search("%s %s\n(.*?)\n"%(col,name), infoStr).group(1)
            else:
                boothInfo[col] = ''

        #product categories
        self.driver = webdriver.Chrome(options = self.options)
        self.driver.get(response.url)
        #need to scroll down
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        categoriesList = [i.text for i in self.driver.find_elements_by_xpath("//h2/a")]
        boothInfo['ProductCategories'] = ','.join(categoriesList)
        time.sleep(3)
        self.driver.close()

        yield boothInfo

