#Unit test for news.py
import os
import unittest
import sys

# 1) Add the **folder** containing News.py, not the file itself.
repo_root = os.path.abspath(r'Python Projects\Stock Bud\Objects')
sys.path.insert(1, repo_root)           

# 2) Only now import our module
from News import News


news={"Title": "Test Title",
            "Description": "Test Description",
            "Date": "2023-10-01",
            "Source": "Test Source"
            }





test_news = News(news['Title'], news['Description'], news['Date'], news['Source'])


#TESTING NEWS CLASS
class TestNews(unittest.TestCase):
    def test_news(self):
        self.assertEqual(test_news.title, news['Title'], msg="Should be equal")
        self.assertEqual(test_news.description, news['Description'], msg="Should be equal")
        self.assertEqual(test_news.date, news['Date'], msg="Should be equal")
        self.assertEqual(test_news.source, news['Source'], msg="Should be equal")
        self.assertIsNone(test_news.data, msg="Should be none")
        test_news.set_data("Test Data")
        self.assertEqual(test_news.data, "Test Data", msg="Should be equal")
        



def main():
    print("Title:", test_news.title)
    print("Description:", test_news.description)
    print("Date:", test_news.date)
    print("Source:", test_news.source)
    unittest.main()
    



if __name__ == "__main__":
    main()






