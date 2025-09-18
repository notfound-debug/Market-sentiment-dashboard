from flask import Flask, jsonify
from flask_cors import CORS
import finnhub
from datetime import datetime, timedelta
import random
import re

from sentiment_analyzer import analyze_sentiment
from anomaly_detector import find_anomalies

app = Flask(__name__)
CORS(app)

API_KEY = 'd35s09pr01qhqkb3ono0d35s09pr01qhqkb3onog' # Make sure your Finnhub API key is here

STOCK_CATEGORIES = {
    "Tech": ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "META", "TSM", "AVGO", "ORCL", "ADBE", "CRM", "CSCO", "INTC", "AMD", "QCOM", "IBM"],
    "Automobile": ["TSLA", "F", "GM", "RIVN", "LCID", "TM", "HMC", "RACE"],
    "Oil & Gas": ["XOM", "CVX", "SHEL", "TTE", "BP", "COP", "EOG", "SLB"],
    "Finance": ["JPM", "BAC", "WFC", "MS", "GS", "C", "V", "MA", "AXP", "BLK", "SCHW", "PYPL"]
}
TRUSTED_SOURCES = ["Reuters", "Associated Press", "Bloomberg", "The Wall Street Journal", "Financial Times", "MarketWatch", "CNBC", "Business Wire", "PR Newswire", "GlobeNewswire", "Accesswire"]
EVENT_KEYWORDS = {"M&A Activity": [r'acquire', r'merger', r'takeover', r'buyout', r'acquisition'], "Earnings Report": [r'earnings', r'revenue', r'quarter', r'profit', r'loss', r'EPS'], "Product Launch": [r'launch', r'unveil', r'release', r'new product'], "Legal/Regulatory": [r'lawsuit', r'investigation', r'SEC', r'DOJ', r'settlement', r'fine'],"Analyst Rating": [r'upgrade', r'downgrade', r'outperform', r'target price']}
MAJOR_TICKERS = set(sum(STOCK_CATEGORIES.values(), []))


def fetch_and_process_news(tickers):
    try:
        finnhub_client = finnhub.Client(api_key=API_KEY)
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        to_date, from_date = today.strftime('%Y-%m-%d'), thirty_days_ago.strftime('%Y-%m-%d')
        
        all_news = []
        # --- NEW: Price cache to avoid redundant API calls ---
        price_cache = {}

        for ticker in tickers:
            news_list = finnhub_client.company_news(ticker, _from=from_date, to=to_date)
            for article in news_list:
                article['ticker'] = ticker
                # --- NEW: Fetch and cache the primary ticker's price ---
                if ticker not in price_cache:
                    try:
                        price_cache[ticker] = finnhub_client.quote(ticker).get('c')
                    except Exception as e:
                        price_cache[ticker] = None # Avoid re-querying on failure
                        print(f"Could not fetch price for primary ticker {ticker}: {e}")
                article['ticker_price'] = price_cache[ticker]

            all_news.extend(news_list)
        
        unique_news = {article['headline']: article for article in all_news}.values()
        shuffled_news, limited_news = list(unique_news), []
        random.shuffle(shuffled_news)
        limited_news = shuffled_news[:50]

        if not limited_news: return []

        for article in limited_news:
            text_to_search = f"{article['headline']} {article['summary']}".lower()
            article['event_type'] = "General News"
            for event, keywords in EVENT_KEYWORDS.items():
                if any(re.search(r'\b' + kw + r'\b', text_to_search) for kw in keywords):
                    article['event_type'] = event
                    break
            
            found_tickers = {t for t in MAJOR_TICKERS if re.search(r'\b' + t + r'\b', article['headline'], re.IGNORECASE)}
            found_tickers.discard(article['ticker'])
            
            mentioned_stocks = []
            for t in found_tickers:
                if t not in price_cache:
                    try:
                        price_cache[t] = finnhub_client.quote(t).get('c')
                    except Exception:
                        price_cache[t] = None
                if price_cache.get(t):
                    mentioned_stocks.append({'ticker': t, 'price': price_cache[t]})
            article['mentioned_stocks'] = mentioned_stocks

            article['sentiment'] = analyze_sentiment(text_to_search)
            article['is_trusted_source'] = article['source'] in TRUSTED_SOURCES
        
        return find_anomalies(limited_news)

    except Exception as e:
        print(f"An error occurred in fetch_and_process_news: {e}")
        return {"error": str(e)}

@app.route('/api/news/category/<string:category_name>', methods=['GET'])
def get_category_news(category_name):
    tickers = STOCK_CATEGORIES.get(category_name)
    if not tickers: return jsonify({"error": "Category not found"}), 404
    data = fetch_and_process_news(tickers)
    if isinstance(data, dict) and "error" in data: return jsonify(data), 500
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)