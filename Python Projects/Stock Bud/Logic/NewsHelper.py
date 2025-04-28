from Logic.NewsExtractor import NewsExtractor
from Logic.Summarizer import NewsInsights



class NewsHelper:
    
    def __init__(self):
        self.extractor = NewsExtractor()
        self.insights = None
        self.lastNews = None
        self.prevNews = {}
        
        
    def __init__(self, openai_api_key=None):
        self.extractor = NewsExtractor()
        self.insights = NewsInsights(openai_api_key=openai_api_key)
        self.lastNews = None
        self.prevNews = {}

    
    #Extracts News Summary from one articles
    def extractNews(self, url):
        news = self.extractor.extractNews(url)
        if news:
            self.lastNews = news
            self.prevNews[news.title] = news
            return news
        return None
    
    #Extracts News summary from the Entire Main page
    def extractNewsFromMainPage(self,url):
        extractedNews=self.extractor.extractNewsFromMainPage(url)
        if extractedNews is None:
            print("Something went wrong")
            return []
        
        else:
            self.prevNews = {}
            for news in extractedNews:
                self.prevNews[news.title] = news
                self.lastNews = news
            return extractedNews
        
    
    #Prints all News summary 
    def printSummarizedNews(self):
        if self.prevNews:
            for title, news in self.prevNews.items():
                print(f"Title: {title}")
                print(f"Description: {news.description}")
                print(f"Date: {news.date}")
                print(f"Source: {news.source}")
                print(f"Data: {news.data}\n")
        else:
            print("No news available.")
        
    #Set the api key
    def setAPIKey(self,openai_api_key):
        self.insights = NewsInsights(openai_api_key=openai_api_key)
    
    
    