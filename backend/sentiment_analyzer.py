from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax

# --- Load Model and Tokenizer ---
# This will download the model from Hugging Face Hub the first time it's run.
MODEL = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using the FinBERT model.
    Returns a dictionary with positive, negative, and neutral scores.
    """
    if not text or not isinstance(text, str):
        # Return neutral sentiment for empty or invalid input
        return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}

    try:
        # Tokenize the text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Get model predictions (logits)
        with torch.no_grad():
            outputs = model(**inputs)

        # Convert logits to probabilities using softmax
        scores = softmax(outputs.logits[0].numpy())

        # The model outputs scores in the order: positive, negative, neutral
        sentiment_scores = {
            'positive': round(float(scores[0]), 4),
            'negative': round(float(scores[1]), 4),
            'neutral': round(float(scores[2]), 4)
        }
        return sentiment_scores

    except Exception as e:
        print(f"Error analyzing sentiment for text: '{text}'. Error: {e}")
        return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0} # Default to neutral on error

# Example of how to use it
if __name__ == '__main__':
    sample_headline = "Big Tech Stocks Soar on Positive Economic News"
    sentiment = analyze_sentiment(sample_headline)
    print(f"Headline: '{sample_headline}'")
    print(f"Sentiment: {sentiment}")

    sample_headline_2 = "New Regulations Could Hurt Corporate Profits"
    sentiment_2 = analyze_sentiment(sample_headline_2)
    print(f"Headline: '{sample_headline_2}'")
    print(f"Sentiment: {sentiment_2}")