import scrapy
from scrapy.http import Request
from news.utils import daterange
from datetime import date, timedelta, datetime
import logging
from news.loaders import NewsLoader
from news.items import NewsItem


class MemeorandumSpider(scrapy.Spider):
    name = 'memeorandum'
    allowed_domains = ['memeorandum.com']

    def start_requests(self):
        start_date = date.fromisoformat('2006-03-01')
        end_date = date.today()
        for day in daterange(start_date, end_date):
            d = day.strftime('%y%m%d')
            h = 'h2100'
            url = 'https://www.memeorandum.com/{0}/{1}'.format(d, h)
            yield Request(url, dont_filter=True, callback=self.parse, cb_kwargs=dict(published_at=day))
            break

    def parse(self, response, published_at):
        scraped_at = datetime.now()
        scraped_url = response.url
        for cluster in response.xpath('//div[@class="clus"]'):
            item_sel = cluster.xpath('div[@class="item"]')
            loader = NewsLoader(item=NewsItem(), selector=item_sel, response=response)
            loader.add_xpath('outlet', 'cite/a/text()')
            loader.add_xpath('outlet_url', 'cite/a/@href')
            loader.add_xpath('author', 'cite/text()')
            loader.add_xpath('description', 'div[@class="ii"]/text()')
            loader.add_xpath('title', './/strong//text()')
            item_url = item_sel.xpath('.//strong//@href').get()
            loader.add_value('url', item_url)
            loader.add_value('type', 'lead')
            loader.add_value('scraped_at', scraped_at)
            loader.add_value('scraped_url', scraped_url)
            loader.add_value('published_at', published_at)
            yield loader.load_item()
            # Other discussions about item
            for discussion in cluster.xpath('div[@class="lnkr"]'):
                d_loader = NewsLoader(item=NewsItem(), selector=discussion)
                d_loader.add_value('parent_url', item_url)
                d_loader.add_xpath('url', 'a/@href')
                d_loader.add_xpath('title', 'a/text()')
                d_loader.add_xpath('author', 'cite/text()')
                d_loader.add_xpath('outlet', 'cite/a/text()')
                d_loader.add_xpath('outlet_url', 'cite/a/@href')
                d_loader.add_value('type', 'discussion')
                d_loader.add_value('scraped_at', scraped_at)
                d_loader.add_value('scraped_url', scraped_url)
                d_loader.add_value('published_at', published_at)
                yield d_loader.load_item()
            # Related Items - Also have authors, descriptions and discussions
            for rel_item in cluster.xpath('.//div[@class="relitems"]/div'):
                r_loader = NewsLoader(item=NewsItem(), selector=rel_item, response=response)
                r_loader.add_xpath('outlet', 'cite/a/text()')
                r_loader.add_xpath('outlet_url', 'cite/a/@href')
                r_loader.add_xpath('author', 'cite/text()')
                r_loader.add_xpath('description', 'strong/a/text()')
                r_loader.add_xpath('title', './/strong/a/text()')
                r_loader.add_value('parent_url', item_url)
                rel_item_url = cluster.xpath('.//strong/a/@href').get()
                r_loader.add_value('url', rel_item_url)
                r_loader.add_value('type', 'related')
                r_loader.add_value('scraped_at', scraped_at)
                r_loader.add_value('scraped_url', scraped_url)
                r_loader.add_value('published_at', published_at)
                yield r_loader.load_item()
                # Other discussions about related item
                for discussion in cluster.xpath('.//div[@class="lnkr"]'):
                    d_loader = NewsLoader(item=NewsItem(), selector=discussion)
                    d_loader.add_value('parent_url', rel_item_url)
                    d_loader.add_xpath('url', 'a/@href')
                    d_loader.add_xpath('title', 'a/text()')
                    d_loader.add_xpath('author', 'cite/text()')
                    d_loader.add_xpath('outlet', 'cite/a/text()')
                    d_loader.add_xpath('outlet_url', 'cite/a/@href')
                    d_loader.add_value('type', 'related_discussion')
                    d_loader.add_value('scraped_at', scraped_at)
                    d_loader.add_value('scraped_url', scraped_url)
                    d_loader.add_value('published_at', published_at)
                    yield d_loader.load_item()
        pass
