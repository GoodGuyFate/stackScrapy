from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(CrawlSpider):
    name = "stackcrawl"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?sort=newest",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=('&page=\d')),
            callback='parse',
            follow=True
        ),
    )
    

    def parse(self, response):
        sel = Selector(response)
        questions = sel.xpath('//div[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="s-link"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="s-link"]/@href').extract()[0]
            yield item