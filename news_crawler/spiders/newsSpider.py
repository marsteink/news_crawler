import scrapy
import feedparser
import time
import pandas as pd
from news_crawler.items import newsArticle
from time import mktime
from datetime import datetime
from bs4 import BeautifulSoup
from newspaper import Article


class newsSpider(scrapy.Spider):

  number_results = 20
  sleep_time = 10

  name = "newsSpider"
  base_url = 'https://news.google.com/rss'
  lang = 'en'
  country = 'US'

  start = '2018-01-01'
  end = '2023-01-01'


  def __init__(self, news_sources=None, search_terms=None, *args, **kwargs):
    super(newsSpider, self).__init__(*args, **kwargs)
    df = pd.read_csv(news_sources)
    search_terms_txt = open(search_terms, "r", encoding='utf-8-sig')
    self.start_urls = self.constructStartURLs(df, search_terms_txt)

  def concatUrl(self, site, search_term):
    try:
      query = 'inurl:' + site + '+' + search_term
      query += '+' + 'after:' + self.start
      query += '+' + 'before:' + self.end
      ceid = '&hl={}-{}&gl={}&ceid={}:{}'.format(self.lang, self.country, self.country, self.country, self.lang)
      URL = self.base_url + '/search?q={}'.format(query) + ceid
      return URL
    except Exception as e:
      print(e)
      raise Exception('Could not concatenate URL', site)

  def constructStartURLs(self, df, search_terms_txt):
    URLs = []
    news_sites = df['site_names'].tolist()
    lines = search_terms_txt.readlines()
    for site in news_sites:
      for search_term in lines:
        if search_term:
          URLs.append(self.concatUrl(site, search_term.strip()))
    return URLs


  """
   Extracts information from the Google News RSS feed results (takes the first *number_results*)
   
   args:
       response (scrapy.http.Response): The response containing Google News RSS feed results.
       
   yields:
       scrapy.http.Request: A request for the actual article using the article_url.
       
   Extracts the following data:
   - title: Google News result title.
   - source: Source of the news article (e.g., CNN.com).
   - article_url: URL used to extract the text and title of the actual article.
   - published: Date of publication according to Google.
  """
  def parse(self, response):
    time.sleep(self.sleep_time)
    data = feedparser.parse(response.text)
    if len(data['entries']) > 0:
      for count, item in enumerate(data['entries']):
        if count > self.number_results:
          break
        else:
          meta = {'search_query': response.request.url,
                  'title': item['title'],
                  'source': item['source']['href'],
                  'article_url': item['link'],
                  'published': datetime.fromtimestamp(mktime(item['published_parsed'])),
                  'article_title': "",
                  'article_text': ""}
          yield scrapy.Request(url=item['link'], callback=self.parse2, meta=meta)
    if len(data['entries']) == 0:
      article = newsArticle()
      article['search_query'] = response.request.url
      source = article['search_query'].split("inurl:")[1]
      source = 'https://www.' + source.split("+")[0]
      article['source'] = source
      article['title'] = None
      article['article_url'] = None
      article['published'] = None
      yield article


  """
      parses an article's HTML content using Beautiful Soup and extracts the text and title
      using the Newspaper library.

      args:
          response (scrapy.http.Response): The response containing the article.

      yields:
          newsArticle: A Scrapy item containing extracted article information.

      yields the newsArticle item with the following fields:
      - 'search_query': The search query used.
      - 'title': Google search result title.
      - 'source': Website of the news agency from which the article originated.
      - 'article_url': Google URL to the article.
      - 'published': Publication date (from Google News search result page).
      - 'article_title': The extracted title of the article.
      - 'article_text': The extracted text content of the article.
      - 'html': HTML page from the article.
      
      Note: If an error occurs during parsing, it will be printed, and 'html' will be set to None.
      """
  def parse2(self, response):
    time.sleep(self.sleep_time)
    article = newsArticle()
    article['search_query'] = response.meta['search_query']
    article['title'] = response.meta['title']
    article['source'] = response.meta['source']
    article['article_url'] = response.meta['article_url']
    article['published'] = response.meta['published']
    article['article_title'] = response.meta['article_title']
    article['article_text'] = response.meta['article_text']
    try:
      article['html'] = BeautifulSoup(response.text, 'lxml')
      try:
        newspaper_article = Article(article['article_url'], language="en")
        newspaper_article.download()
        newspaper_article.html = str(article['html'])
        newspaper_article.parse()
        if newspaper_article.title:
          article['article_title'] = newspaper_article.title
          if (newspaper_article.text):
            article['article_text'] = newspaper_article.text
      except Exception as e:
        print(e)
    except Exception as e:
      article['html'] = None
      print(e)
    yield article