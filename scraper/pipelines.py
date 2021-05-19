# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from news import settings
import logging
from news.items import NewsItem

class DatabasePipeline(object):
    def __init__(self, database_settings):
        print(database_settings)
        self.database_settings = database_settings

    @classmethod
    def from_crawler(cls, crawler):
        database_settings = crawler.settings.getdict("DB_SETTINGS")
        if not database_settings: # if we don't define db config in settings
            raise NotConfigured # then reaise error
        return cls(database_settings) # returning pipeline instance

    def open_spider(self, spider):
        self.engine = create_engine(URL.create(**self.database_settings))

    def process_item(self, item, spider):
        data = {
                "url":item.get("url")
                ,"author":item.get("author")
                ,"title":item.get("title")
                ,"description":item.get("description")
                ,"outlet":item.get("outlet")
                ,"outlet_url":item.get("outlet_url")
                ,"type":item.get("type")
                ,"scraped_at":item.get("scraped_at")
                ,"scraped_url":item.get("scraped_url")
                ,"parent_url":item.get("parent_url")
                ,"published_at":item.get("published_at")
            }
        query = text("""INSERT INTO news (
                url
                ,author
                ,title
                ,description
                ,outlet
                ,outlet_url
                ,type
                ,scraped_at
                ,scraped_url
                ,parent_url
                ,published_at
            ) VALUES (:url,:author,:title,:description,:outlet,:outlet_url,:type,:scraped_at,:scraped_url, :parent_url, :published_at)""")
        with self.engine.connect() as conn:
            conn.execute(query,data)
        return item
