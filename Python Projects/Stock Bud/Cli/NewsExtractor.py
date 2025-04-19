#Author: Daniel Nwogo
#Date: 2023-10-04
#imports
import News
from newspaper import Article

DEFAULT_NEWS_URL="https://ca.finance.yahoo.com/news/nvidias-2025-has-been-anything-but-easy-and-its-going-to-get-tougher-171847622.html"



class NewsExtractor:
    
    def __init__(self):
        #last news article
        self.lastNews= None
        #Stores the title and the News DSO
        self.prevNews = {}



        
        
    #Returns a news article objects
    def extractNews(self,url):
        #Perform configurations on article
        article=Article(url)
        article.download()
        article.parse()
        article.nlp()
        

        
        #News object
        news=News(
            title=article.title,
            description=article.summary,
            date=article.publish_date,
            source=article.source_url,
            data=article.text.strip()
        )
        
        self.lastNews = news
        self.prevNews[news.title] = news
        return news

    #
    #Used to extract multiple news articles from a list of urls
    def extractMultipleNews(self, urls):
        newsList = []
        for url in urls:
            news = self.extractNews(url)
            newsList.append(news)
        return newsList
    
    #Used to extract multiple urls from a News homepage
    def extractMultipleUrls(self, url):
        newsList = []
        for url in urls:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            news = News(
                title=article.title,
                description=article.summary,
                date=article.publish_date,
                source=article.source_url,
                data=article.text.strip()
            )
            
            self.lastNews = news
            self.prevNews[news.title] = news
            newsList.append(news)
        return newsList
        
        
        