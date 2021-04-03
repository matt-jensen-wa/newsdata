# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    outlet = scrapy.Field()
    outlet_url = scrapy.Field()
    parent_url = scrapy.Field()
    published_at = scrapy.Field()
    type = scrapy.Field()
    scraped_at = scrapy.Field()
    scraped_url = scrapy.Field()

