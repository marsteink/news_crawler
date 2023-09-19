# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class newsArticle(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()              # title in the search result page (not of actual article)
    article_url = scrapy.Field()
    published = scrapy.Field()
    article_title = scrapy.Field()  # parsed title on the actual article site
    article_text = scrapy.Field()
    html = scrapy.Field()
    search_query = scrapy.Field()

