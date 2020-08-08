import json
import scrapy
from datetime import datetime

OUTPUT_FILENAME = 'sendo.json'

class VnExpressSpider(scrapy.Spider):
    name = 'sendo1'
    allowed_domains = ['sendo.vn']
    crawled_count = 0
    start_urls = ['https://www.sendo.vn/',]
    def parse(self, response):
        if response.status == 200 and response.css('div.container div.productGallery_2-ET'):
            print('Crawling from:', response.url)
            data = {
                'link': response.url,
                'title': response.css('h1.productName_3Cdc::text').get(),
                'price': response.css('strong.currentPrice_2zpf::text').get(),
                'description': response.css('meta[name="description"]::attr("content")').get(),
                'number_of_rating': response.css('span.rateNumber_RH_t > em::text').getall()[1],
                'number_of_ordered': response.css('div.order_2orB::text').getall()[2],
                'tag': [k.strip() for k in response.css('meta[property="keywords"]::attr("content")').get().split(',')],

            }
            with open(OUTPUT_FILENAME, 'w', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.crawled_count += 1
                self.crawler.stats.set_value('crawled_count', self.crawled_count)
                print('SUCCESS:', response.url)
        yield from response.follow_all(css='a[href^="/"]::attr(href)',
                                       callback=self.parse)



