import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(CrawlSpider):
    name = "vnexpress"
    start_urls = [
        'https://vnexpress.net'
    ]
    rules = (
        Rule(LinkExtractor(
            allow=('^https:\/\/vnexpress.net.*\d{7}.html$')
        ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        file_name = response.url.split('/')[-1]
        file_name = file_name.replace('.html', '.txt')
        with open("vnexpress/%s" % file_name, 'a', encoding='utf-8') as f:
            title = response.xpath('//meta[@name="twitter:title"]/@content').get() + "<end_of_title>\n"
            f.write(title)
            description = response.xpath('//p[@class="description"]/text()').get() + "<end_of_description>\n"
            f.write(description)
            content = response.xpath('//p[contains(@class,Normal)]/text()').extract()
            content1 = '\n'.join(content)
            f.write(content1)
