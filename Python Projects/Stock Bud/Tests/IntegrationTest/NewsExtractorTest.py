from newspaper import Article
DEFAULT_NEWS_URL="https://ca.finance.yahoo.com/news/nvidias-2025-has-been-anything-but-easy-and-its-going-to-get-tougher-171847622.html"

# RANDOM_NEWS_ARTICLE_1='https://www.cnbc.com/2025/04/18/trump-says-government-to-change-service-regulations-for-career-government-employees.html'
RANDOM_NEWS_ARTICLE_1=DEFAULT_NEWS_URL

article_1 = Article(RANDOM_NEWS_ARTICLE_1)
article_1.download()
article_1.parse()
print(article_1.text.strip())