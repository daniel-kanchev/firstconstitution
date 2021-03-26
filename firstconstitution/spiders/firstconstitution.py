import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from firstconstitution.items import Article


class FirstconstitutionSpider(scrapy.Spider):
    name = 'firstconstitution'
    start_urls = ['https://www.1stconstitution.com/news-and-events/']

    def parse(self, response):
        links = response.xpath('//div[@class="blog-list-item-excerpt"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="entry-title"]/h1//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//li[@class="meta-date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="entry-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
