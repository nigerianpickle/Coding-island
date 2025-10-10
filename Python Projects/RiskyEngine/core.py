import praw

STOCK_CACHE={}


reddit = praw.Reddit(
    client_id="YEes_pm7hmX7Eq9ccRs4QQ",
    client_secret="SQMET9PUYGQRX0rluHDGKrmznQ8Waw",
    user_agent="Risky Engine heart"
)





wallStreetBets = reddit.subreddit("wallstreetbets")



for post in wallStreetBets.hot(limit=30):
    print(post.title, post.score, post.url)