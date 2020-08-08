import json
import scrapy
from datetime import datetime

OUTPUT_FILENAME = 'vnexpress_data.json'


class VnExpressSpider(scrapy.Spider):
    name = 'vnexpress2'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net', ]
    crawled_count = 0

    def parse(self, response):
       if response.status == 200 and response.css('meta[name="tt_page_type"]::attr("content")').get() == 'article':
           print('Crawling from:', response.url)
           data = {
               'link': response.url,
               'title': response.css('h1.title-detail::text').get(),
               'description': response.css('p.description::text').get(),
               'content': "\n".join(
                   [''.join(c.css('*::text').getall()) for c in response.css('article.fck_detail p.Normal')]),
               'category': response.css('ul.breadcrumb > li > a::attr("title")').get(),
               'pub_date': response.css('span.date::text').get(),
               'tags': [k.strip() for k in response.css('meta[name="its_tag"]::attr("content")').get().split(',')],
           }
           with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
               f.write(json.dumps(data, ensure_ascii=False))
               f.write('\n')
               self.crawled_count += 1
               self.crawler.stats.set_value('crawled_count', self.crawled_count)
               print('SUCCESS:', response.url)
       yield from response.follow_all(css='a[href^="https://vnexpress.net"]::attr(href), a[href^="/"]::attr(href)',
                                      callback=self.parse)



