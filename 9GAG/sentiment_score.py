import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

pd.options.mode.chained_assignment = None  # default='warn'

def get_senti_score(file):
    sent = SentimentIntensityAnalyzer()
    df = pd.read_csv(file)
    text = df['text']
    df['Neutrality_Score'] = 0
    df['Positivity_Score'] = 0
    df['Negativity_Score'] = 0
    df['sentiment'] = " "
    for index, comment in zip(range(0, len(text)), text):
        if isinstance(comment, str) and len(
                comment) > 2 and comment != 'attachments' and comment != 'media' and comment != 'nan':
            polarity = sent.polarity_scores(comment)
            neg, pos, neu = polarity['neg'], polarity['pos'],  polarity['neu']
            df['Positivity_Score'].iloc[index] = pos
            df['Negativity_Score'].iloc[index] = neg
            df['Neutrality_Score'].iloc[index] = neu
            if pos > neg and pos > neu:
                df['sentiment'].iloc[index] = "Positive"
            elif neg > pos and neg > neu:
                df['sentiment'].iloc[index] = "Negative"
            else:
                df['sentiment'].iloc[index] = "Neutral"

    df.to_csv(file, index=False)