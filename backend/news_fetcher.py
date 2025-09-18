import finnhub
import os
from datetime import datetime, timedelta
from sentiment_analyzer import analyze_sentiment
from anomaly_detector import find_anomalies 

# --- Configuration ---
API_KEY = 'd35s09pr01qhqkb3ono0d35s09pr01qhqkb3onog' 
STOCK_TICKER = 'AAPL'

def process_stock_news(ticker):
    try:
        # 1. FETCH NEWS
        finnhub_client = finnhub.Client(api_key=API_KEY)
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30) # Fetch more articles for better stats
        to_date = today.strftime('%Y-%m-%d')
        from_date = thirty_days_ago.strftime('%Y-%m-%d')

        print(f"Fetching news for {ticker} from {from_date} to {to_date}...")
        news_list = finnhub_client.company_news(ticker, _from=from_date, to=to_date)

        if not news_list:
            print("No news found for the specified period.")
            return []

        # 2. ANALYZE SENTIMENT FOR ALL ARTICLES
        print(f"Analyzing sentiment for {len(news_list)} articles...")
        for article in news_list:
            article['sentiment'] = analyze_sentiment(article['headline'])

        # 3. DETECT ANOMALIES
        print("Detecting anomalies...")
        articles_with_anomalies = find_anomalies(news_list)

        # 4. PRINT RESULTS
        for article in articles_with_anomalies:
            print("---")
            print(f"Headline: {article['headline']}")
            print(f"Sentiment: {article['sentiment']}")
            print(f"Polarity Score: {article['polarity_score']}")

            if article['is_anomaly']:
                print(">>> ANOMALY DETECTED! <<<")

        return articles_with_anomalies

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    process_stock_news(STOCK_TICKER)