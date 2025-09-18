import numpy as np

# This threshold determines how many standard deviations from the mean
# a score must be to be considered an anomaly. You can tune this value.
DEVIATION_THRESHOLD = 1.5 

def find_anomalies(articles_with_sentiment):
    """
    Identifies sentiment anomalies in a list of articles.

    Args:
        articles_with_sentiment (list): A list of article dicts, 
                                        each must have a 'sentiment' key.

    Returns:
        list: The same list of articles, with an added 'is_anomaly' boolean
              and a 'polarity_score' float for each article.
    """
    if not articles_with_sentiment:
        return []

    # 1. Calculate the polarity score for each article
    for article in articles_with_sentiment:
        sentiment = article.get('sentiment', {'positive': 0, 'negative': 0})
        polarity_score = sentiment['positive'] - sentiment['negative']
        article['polarity_score'] = round(polarity_score, 4)

    # 2. Get a list of all scores for statistical analysis
    scores = [article['polarity_score'] for article in articles_with_sentiment]

    # 3. Calculate mean and standard deviation
    mean_score = np.mean(scores)
    std_dev = np.std(scores)

    print(f"\n--- Anomaly Detection Stats ---")
    print(f"Mean Polarity Score: {mean_score:.4f}")
    print(f"Standard Deviation: {std_dev:.4f}")
    print(f"Threshold (Mean +/- {DEVIATION_THRESHOLD}*SD): {mean_score - DEVIATION_THRESHOLD * std_dev:.4f} to {mean_score + DEVIATION_THRESHOLD * std_dev:.4f}\n")

    # 4. Flag anomalies
    for article in articles_with_sentiment:
        score = article['polarity_score']
        is_anomaly = (score > mean_score + (DEVIATION_THRESHOLD * std_dev)) or \
                     (score < mean_score - (DEVIATION_THRESHOLD * std_dev))
        article['is_anomaly'] = bool(is_anomaly)

    return articles_with_sentiment