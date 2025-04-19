#Author: Daniel Nwogo
#Date: 2023-10-04
#imports
from News import News
import newspaper
from newspaper import Article,Config

DEFAULT_NEWS_URL="https://ca.finance.yahoo.com/news/nvidias-2025-has-been-anything-but-easy-and-its-going-to-get-tougher-171847622.html"


class NewsExtractor:
    
    def __init__(self):
        #last news article
        self.lastNews= None
        #Stores the title and the News DSO
        self.prevNews = {}



    def extractTitleFromUrl(self, url):
        extractedTitle = url[32:-15]
        extractedTitle = extractedTitle.replace("-", " ")

        
    #Returns a news article objects
    def extractNews(self,url):
        #Perform configurations on article
        article=Article(url)
        article.download()
        article.parse()
        # article.nlp()
        

        
        #News object
        if article.title == None:
            news=News(
                title=self.extractTitleFromUrl(url),
                description=article.summary,
                date=article.publish_date,
                source=article.source_url,
                data=article.text.strip()
            )
        elif article.publish_date == None:
            news=News(
                title=article.title,
                description=article.summary,
                date="Unknown",
                source=article.source_url,
                data=article.text.strip()
            )
        elif article.source_url == None:
            news=News(
                title=article.title,
                description=article.summary,
                date=article.publish_date,
                source="Unknown",
                data=article.text.strip()
            )   
        elif article.text == None:
            news=News(
                title=article.title,
                description=article.summary,
                date=article.publish_date,
                source=article.source_url,
                data="Unknown"
            )
        elif article.text == "":
            news=News(
                title=article.title,
                description=article.summary,
                date=article.publish_date,
                source=article.source_url,
                data="Unknown"
            )
        else:
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
            self.prevNews[news.title] = news
        return newsList
    
    #Used to extract multiple urls from a News homepage
    def extractMultipleUrls(self, url):
        urlList = []
        

        news_paper=newspaper.build(url, memoize_articles=False)
        
        for article in news_paper.articles:
            #skip
            if article.url in urlList:
                continue
            

            urlList.append(article.url)
        
        return urlList
    
    def extractNewsFromMainPage(self, url):
        urlList = self.extractMultipleUrls(url)
        
        newsList= self.extractMultipleNews(urlList)
        
        #List of each news article
        return newsList
        
    def printNews(self):
        for news in self.prevNews:
            print("Title:", news.title)
            print("Description:", news.description)
            print("Date:", news.date)
            print("Source:", news.source)
            print("Data:", news.data)
            print("")
            
            
#Test the extractor
testExtractor = NewsExtractor()
testExtractor.extractNews("https://www.cnbc.com/")

            
            
            

        
        
        

testExtractor = NewsExtractor()
testExtractor.extractNewsFromMainPage("https://ca.finance.yahoo.com/")
