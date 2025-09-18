# Market Sentiment & Anomaly Detection Dashboard

This is a full-stack web application designed to serve as a powerful decision-support tool for investors and financial analysts. It automates the task of consuming and interpreting vast amounts of real-time financial news by leveraging a specialized financial NLP model to analyze market sentiment and detect statistically significant anomalies.


<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/e0065938-7062-498d-9517-f0e789d26c9a" alt="Dashboard Overview" width="420">
      <br>
      <em>Dashboard view with filters for category and event type.</em>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/1530a7e6-5bb7-45d2-8a52-a1914b0528e9" alt="Sentiment Analysis in Action" width="420">
      <br>
      <em>Sentiment analysis for the "Oil & Gas" sector showing positive and negative anomalies.</em>
    </td>
  </tr>
</table>

---

## Key Features

- **Real-Time News Aggregation:** Fetches the latest financial news from dozens of sources for major stocks across different industry sectors (Tech, Finance, etc.).
- **Advanced Sentiment Analysis:** Integrates a pre-trained **FinBERT** model, specifically tuned for financial language, to accurately classify news sentiment as positive, negative, or neutral.
- **Statistical Anomaly Detection:** Implements a statistical model to flag articles with unusually strong positive or negative sentiment, acting as an early-warning system for potentially market-moving news.
- **Dynamic Filtering & Sorting:** Features a dynamic and responsive UI with controls to sort news by relevance (trusted sources first) or date, and to filter by stock category and event type (e.g., M&A, Earnings Reports).
- **Rich Data Context:** Automatically extracts other mentioned company tickers from news articles and fetches their live stock prices, providing invaluable context within a single view.
- **Event Classification:** Uses keyword analysis to categorize news into distinct event types, allowing users to focus on specific kinds of information.

---

## Tech Stack

**Backend:**
- **Language:** Python
- **Framework:** Flask
- **Machine Learning:** `transformers` (Hugging Face) for FinBERT, `scikit-learn`
- **Data Analysis:** Pandas, NumPy
- **API:** Finnhub API for news and stock price data

**Frontend:**
- **Library:** React.js
- **UI:** Material-UI (MUI)
- **Styling:** Emotion, CSS
- **Date Handling:** `date-fns`

---

## Setup and Installation

To run this project locally, follow these steps:

**1. Clone the Repository**
```bash
git clone [https://github.com/notfound-debug/Market-sentiment-dashboard.git](https://github.com/notfound-debug/Market-sentiment-dashboard.git)
cd Market-sentiment-dashboard
