# Author: Daniel Nwogo
# Date:   2023-10-04

from News import News
import newspaper
from newspaper import Article

DEFAULT_NEWS_URL = "https://ca.finance.yahoo.com/news/nvidias-2025-has-been-anything-but-easy-and-its-going-to-get-tougher-171847622.html"
NEWS_LIMIT=3

class NewsExtractor:
    
    def __init__(self):
        self.lastNews = None
        self.prevNews = {}

    def extractTitleFromUrl(self, url):
        # derive a human‑readable title from the URL
        title = url[32:-15].replace("-", " ").strip()
        return title

    def extractNews(self, url):
        # download & parse without NLP/summary
        article = Article(url)
        article.download()
        article.parse()

        # use real values or sensible fallbacks
        title       = article.title        or self.extractTitleFromUrl(url)
        description = ""  # summary removed
        date        = article.publish_date or "Unknown"
        source      = article.source_url   or "Unknown"
        data        = article.text.strip() or "Unknown"

        news = News(title, description, date, source, data)
        self.lastNews = news
        self.prevNews[title] = news
        return news

    #
    def extractMultipleNews(self, urls):
        news_list = []
        for url in urls:
            news_list.append(self.extractNews(url))
        return news_list

    def extractMultipleUrls(self, url):
        print("Building a newspaper object…")
        paper = newspaper.build(url, memoize_articles=False)

        print("Gathering article URLs…")
        url_list = []
        for article in paper.articles:
            if article.url not in url_list:
                url_list.append(article.url)
            if len(url_list) == NEWS_LIMIT:
                break

        print(f"Collected {len(url_list)} URLs.")
        return url_list

    def extractNewsFromMainPage(self, url):
        #urls give us a list of article URLs
        #then we can extract the news from each URL
        urls = self.extractMultipleUrls(url)
        return self.extractMultipleNews(urls)

    def printNews(self):
        for title, news in self.prevNews.items():
            print(f"Title:       {news.get_title()}")
            # description is always empty now
            print(f"Description: {news.get_description()}")
            
            date = news.get_date()
            if hasattr(date, "strftime"):
                date_str = date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = date
            print(f"Date:        {date_str}")
            
            print(f"Source:      {news.get_source()}")
            print(f"Data:        {news.data}")
            print()


if __name__ == "__main__":
    extractor = NewsExtractor()
    extractor.extractNewsFromMainPage("https://www.cnbc.com/")
    extractor.printNews()


