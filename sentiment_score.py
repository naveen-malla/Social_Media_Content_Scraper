import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_senti_score(file):
    sent = SentimentIntensityAnalyzer()
    df = pd.read_csv(file)
    text = df['text']
    df['sentiment_score'] = 0
    for index, comment in zip(range(0, len(text)), text):
        if isinstance(comment, str) and len(
                comment) > 2 and comment != 'attachments' and comment != 'media' and comment != 'nan' and df['type'].iloc[index] == 'text':
            polarity = sent.polarity_scores(comment)
            df['sentiment_score'].iloc[index] = polarity['compound']
            print(polarity, comment)
    df.to_csv(file)