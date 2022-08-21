import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

pd.options.mode.chained_assignment = None  # default='warn'

def get_senti_score(file):
    sent = SentimentIntensityAnalyzer()
    df = pd.read_csv(file)
    text = df['text']
    df['sentiment_score'] = 0
    df['sentiment'] = " "
    for index, comment in zip(range(0, len(text)), text):
        if isinstance(comment, str) and len(
                comment) > 2 and comment != 'attachments' and comment != 'media' and comment != 'nan' and df['type'].iloc[index] == 'text':
            polarity = sent.polarity_scores(comment)
            neg, pos, neu = polarity['neg'], polarity['pos'],  polarity['neu']
            if pos > neg and pos > neu:
                df['sentiment'].iloc[index] = "Positive"
                df['sentiment_score'].iloc[index] = str(polarity)
            elif neg > pos and neg > neu:
                df['sentiment'].iloc[index] = "Negative"
                df['sentiment_score'].iloc[index] = str(polarity)
            else:
                df['sentiment'].iloc[index] = "Neutral"
                df['sentiment_score'].iloc[index] = str(polarity)

    df.to_csv(file, index=False)