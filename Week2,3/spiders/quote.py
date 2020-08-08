import json
import scrapy
from datetime import datetime

OUTPUT_FILENAME = 'quote.txt'

class QuoteSpider(scrapy.Spider):
    name = 'quote'

    crawled_count = 0
    start_urls = ['http://quotes.toscrape.com/',]
    def parse(self, response):
        for quote in response.css('div.quote'):
            data = {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }
            with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.crawled_count += 1
                self.crawler.stats.set_value('crawled_count', self.crawled_count)
        yield from response.follow_all(css='li.next > a::attr(href)',
                                       callback=self.parse)



