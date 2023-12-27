import feedparser

def fetch_latest_tech_news(feed_url='https://techcrunch.com/feed', num_articles=10):
    # Parse the RSS feed
    news_feed = feedparser.parse(feed_url)
    
    # Extract the news articles
    articles = news_feed.entries[:num_articles]
    
    # Return the articles
    return articles
