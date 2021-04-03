from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader
import unidecode 

def trim_author(x):
    return x.strip().strip(':/').strip()

def trim(x):
    return x.strip().strip('-').strip()

def date_to_string(x):
    return x.strftime('%Y-%m-%d %H:%M:%S')

class NewsLoader(ItemLoader):
    url_out = TakeFirst()

    parent_url_out = TakeFirst()

    published_at_in = MapCompose(date_to_string)
    published_at_out = TakeFirst()

    author_in = MapCompose(trim_author)
    author_out = TakeFirst()

    title_in = MapCompose(unidecode.unidecode, trim)
    title_out = Join()

    description_in = MapCompose(unidecode.unidecode, trim)
    description_out = Join()

    outlet_out = TakeFirst()
    outlet_url_out = TakeFirst()

    type_out = TakeFirst()

    scraped_at_in = MapCompose(date_to_string)
    scraped_at_out = TakeFirst()
    scraped_url_out = TakeFirst()


