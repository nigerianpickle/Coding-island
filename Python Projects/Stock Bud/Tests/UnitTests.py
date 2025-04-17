#Unit test for news.py
import unittest
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'Python Projects\Stock Bud\Objects\News.py')



news={"Title": "Test Title",
            "Description": "Test Description",
            "Date": "2023-10-01",
            "Source": "Test Source"}




test_news = News(news['Title'], news['Description'], news['Date'], news['Source'])






#TESTING NEWS CLASS
unittest.Testcase.assertEqual(test_news.title, news['Title'])
unittest.Testcase.assertEqual(test_news.description, news['Description'])
unittest.Testcase.assertEqual(test_news.date,news['Date'])
unittest.Testcase.assertEqual(test_news.source,news['Source'])



