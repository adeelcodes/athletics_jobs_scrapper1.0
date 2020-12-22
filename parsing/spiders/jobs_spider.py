import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from typing import List


class JobsSpider(scrapy.Spider):
    name = "ncaamarket-jobs"

    def start_requests(self):
        urls = [
            'https://ncaamarket.ncaa.org/jobs/?page=1',
            'https://ncaamarket.ncaa.org/jobs/?page=2',
            'https://ncaamarket.ncaa.org/jobs/?page=3',
            'https://ncaamarket.ncaa.org/jobs/?page=4',
            'https://ncaamarket.ncaa.org/jobs/?page=5',
            'https://ncaamarket.ncaa.org/jobs/?page=6',
            'https://ncaamarket.ncaa.org/jobs/?page=7',
            'https://ncaamarket.ncaa.org/jobs/?page=8',
            'https://ncaamarket.ncaa.org/jobs/?page=9',
            'https://ncaamarket.ncaa.org/jobs/?page=10',
            'https://ncaamarket.ncaa.org/jobs/?page=11',
            'https://ncaamarket.ncaa.org/jobs/?page=12',
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                errback=self.errback_httpbin,
                callback=self.parse
            )

    def parse(self, response):
        for job in response.css('div.bti-ui-job-detail-container'):
            yield from response.follow_all(
                urls=job.css('div.bti-ui-job-result-detail-title a'),
                callback=self.parse_job,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    @staticmethod
    def extract_posted_date(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('::text').get()).lower() == 'posted:':
                return response[key+1].css('::text').get().strip()
        return ''

    @staticmethod
    def extract_job_location(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('::text').get()).lower() == 'location:':
                return response[key+1].css('span::text').get()
        return ''

    @staticmethod
    def extract_job_type(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('::text').get()).lower() == 'type:':
                return response[key+1].css('div::text').get()
        return ''

    @staticmethod
    def extract_job_sector(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('div::text').get()).lower() == 'sector:':
                return response[key + 1].css('div::text').get()
        return ''

    @staticmethod
    def extract_job_categories(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('div::text').get()).lower() in ('categories:', 'category:'):
                return response[key + 1].css('div::text').get()
        return ''

    @staticmethod
    def extract_required_education(response) -> str:
        for key, item in enumerate(response):
            if str(item.css('div::text').get()).lower() in ('preferred education:', 'required education:'):
                return response[key + 1].css('div::text').get()
        return ''

    @staticmethod
    def extract_all_text_from_table(selector) -> str:
        result_text = ''
        for row in selector.xpath('.//text()').extract():
            if row != ' ':
                encoding_sting = row.encode('utf-8')
                result_text += encoding_sting.decode()
        return result_text

    def parse_job(self, response):
        yield {
            'url': response.url, # 1
            'job_title': response.css('h1.bti-jd-title::text').extract_first(), # 2
            'employer_name': response.css('h2.bti-jd-employer-title::text').extract_first().strip(), # 3
            'job_description': self.extract_all_text_from_table(response.css('div.bti-jd-description table tr td')), # 4
            'job_qualifications': self.extract_all_text_from_table( # 5
                response.css('div.bti-jd-requirements table tr td')),
            'job_posted_date': self.extract_posted_date(response.css('div.bti-jd-details-action div')), # 6
            'job_location': self.extract_job_location(response.css('div.bti-jd-details-action div')), # 7
            'job_type': self.extract_job_type(response.css('div.bti-jd-details-other div')), # 8
            'job_sector': self.extract_job_sector(response.css('div.bti-jd-details-other div')), # 9
            'job_categories': self.extract_job_categories(response.css('div.bti-jd-details-other div')), # 10
            'required_education': self.extract_required_education(response.css('div.bti-jd-details-other div')), # 11
            'about_employer': response.css('div.bti-jd-employer-info::text').get() # 12
        }
