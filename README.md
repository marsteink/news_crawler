# News Crawler
`news_crawler` is a python script that allows you to find articles on a specific topic from various news sources. It relies on the Google News RSS feed at 'https://news.google.com/rss' for search results. The crawler stores the results in a .csv file with the following structure:

- **source**: The website of the news agency from which the article originated.
- **title**: Google search result title.
- **article_url**: Google URL to the article.
- **published**: Publication date (from Google News search result page).
- **article_title**: Title of the article.
- **article_text**: Body of the article.
- **html**: HTML page from the article.
- **search_query**: The search query used.

### Example Use Cases

Find news articles about the Super Bowl from various US news outlets.\
Find news articles on sustainable investment from various US news outlets.\
Retrieve news articles related to the COVID-19 pandemic from selected news sources.

### How to Run

1. Open your terminal in the `spiders` folder.
2. Run the following command:

```bash
scrapy runspider newsSpider.py -o articles.csv -a news_sources=news_sources.csv -a search_terms=search_terms.txt
```
- **articles.csv**: The file where the results will be stored.
- **news_sources.csv**: A .csv file with a `site_names` column containing domain names of the news outlets you want to retrieve articles from.
- **search_terms.txt**: A text file containing search terms, with each term on a separate line. Ensure the correct format, e.g., for "Socially responsible investing SRI" use the search term "socially+responsible+investing+SRI"

### Documentation
`newsSpider.py`
newsSpider.py performs searches on the Google News RSS feed by combining each search term with each news source. It does this by constructing a search URL in the following format:
https://news.google.com/rss/search?q=inurl:cnn.com+Environment+Social+and+Governance+ESG+after:2018-01-01+before:2023-01-01&hl=en-US&gl=US&ceid=US:en

In this URL example, `cnn.com` is the news source, and `Environment+Social+and+Governance+ESG` is the search term. You can see that it includes parameters like the publication date (after and before dates), language (hl), and region (gl) for more precise results.

Additionally, you can customize other parameters besides `news_sources` and `search_terms`:
- **number_results**: Defines the number of search results the spider should crawl on every search from Google News RSS feed (default is 20).
- **sleep_time**: This parameter controls the time interval between consecutive searches performed by `newsSpider.py`. The default sleep time is 10 seconds.
- **lang** and **country** settings.
- **start** and **end** to specify a date range for the search, with default values of `start='2018-01-01'` and `end='2023-01-01'`.

In essence, for each combination of search terms and news sources, `newsSpider.py` creates a custom search URL to fetch relevant news articles. This allows you to tailor your searches to specific criteria and obtain the desired results.

Note: If a search query does not yield any results on the Google search result page, an entry is still written to `articles.csv`. However, in this case, all fields except `source` and `search_query` will be null.


### News Sources
The `news_sources.csv` file included in this project contains a list of news sources gathered from AllSides.com, along with information about their political bias. This file is used to specify the sources from which news articles will be fetched.

To specify the news sources for crawling, you only need to provide a CSV file with a single column named `site_names`. The crawler will use the information in this column to search for articles from the specified sources.

### Built With
[feedparser](https://github.com/kurtmckee/feedparser)\
[beautifulsoup](https://pypi.org/project/beautifulsoup4/)\
[scrapy](https://scrapy.org/)

### License
This project uses portions of code from the [pygooglenews](https://github.com/kotartemiy/pygooglenews) by [Artem Bugara](https://github.com/kotartemiy) under the MIT License.