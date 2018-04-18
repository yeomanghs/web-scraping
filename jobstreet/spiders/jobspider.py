from jobstreet.items import Job
import scrapy
import re

class tutorial(scrapy.Spider):
    name = "job"
    allowed_domain = ["jobstreet.com"]
    start_urls= ["https://www.jobstreet.com.my/en/job-search/job-vacancy.php?key=&location=50300&specialization=&area=&salary=&ojs=3&src=12"]

    def parse(self,response):
        #jobinfo = Job()
        #position = response.xpath('//h2/text()').extract()
        #companyName = response.xpath('//span[@itemprop = "name"]/text()').extract()
        link = response.xpath('//a[@class = "position-title-link"]/@href').extract()
        #for i in zip(position,companyName):
        #    jobinfo['position'] = i[0]
        #    jobinfo['companyName'] = i[1]
        #    yield jobinfo
        for i in link:
            jobinfo = Job()
            jobinfo['link'] = i
            request = scrapy.Request(i,callback = self.parseDetails)
            request.meta['job'] = jobinfo
            yield request

    def parseDetails(self,response):
        jobinfo = response.meta['job']
        jobinfo['publicTrans'] = response.xpath('//ul[@id = "poi_train1"]/li/text()').extract()
        jobinfo['position'] = response.xpath('//h1[@id = "position_title"]/text()').extract()
        jobinfo['yearsExp'] = [re.sub('\t|\n','',i).strip() for i in response.xpath('//*[@id="years_of_experience"]/text()').extract()
                               if re.sub('\t|\n','',i).strip()!='']
        jobinfo['companyName'] = [re.sub('\t|\n','',i).strip() for i in response.xpath('//div[@id = "company_name"]/a/text()\
                                    |//*[@id="company_name"]/text()').extract() if re.sub('\t|\n','',i).strip()!='']
        jobinfo['address'] = response.xpath('//p[@id = "address"]/text()').extract()
        jobinfo['industry'] = response.xpath('//p[@id = "company_industry"]/text()').extract()
        jobinfo['companySize'] = response.xpath('//p[@id = "company_size"]/text()').extract()
        jobinfo['benefit'] = [re.sub('\t|\n','',i).strip() for i in response.xpath('//*[@id="work_environment_benefits"]/text()').extract()
                              if re.sub('\t|\n','',i).strip()!='']
        jobinfo['jobDescription'] = response.xpath('//*[@id="job_description"]/div[1]/div[3]/ul/li/text()\
                                                   |//*[@id="job_description"]/ul[2]/li/text()\
                                                   |//*[@id="job_description"]/div[2]/div/div[3]/ul/li/text()').extract()
        jobinfo['postingDate'] = response.xpath('//*[@id="posting_date"]/span/text()').extract()
        yield jobinfo