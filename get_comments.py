import requests
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

def save_comments(post):
    comments1 = post + "_comments.csv"
    replies1 = post + "_replies.csv"

    r = requests.get(
        f'https://comment-cdn.9gag.com/v2/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&count=100&type=hot&url=http%3A%2F%2F9gag.com%2Fgag%2F{post}&origin=https%3A%2F%2F9gag.com')
    data = r.json()
    df = pd.DataFrame(data['payload']['comments'])
    df.rename(columns={'commentId': 'parent'}, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.to_csv(comments1, mode='w', index=False)
    print(comments1, "saved")

    if data['payload']['next'] is not None:
        nextpage = data['payload']['next']
        while True:
            r2 = requests.get(
                f'https://comment-cdn.9gag.com/v2/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&count=100&{nextpage}')
            data2 = r2.json()
            dfn = pd.DataFrame(data2['payload']['comments'])
            dfn.rename(columns={'commentId': 'parent'}, inplace=True)
            dfn['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            dfn.to_csv(comments1, mode='a', index=False)
            print(comments1, "saving", end="\r", )

            if (data2['payload']['next']) is None:
                break
            nextpage = data2['payload']['next']

    replies = []
    for i in data['payload']['comments']:
        commentId = i['commentId']
        r1 = requests.get(
            f'https://comment-cdn.9gag.com/v2/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&count=100&type=old&url=http%3A%2F%2F9gag.com%2Fgag%2F{post}&commentId={commentId}&level=2&origin=https%3A%2F%2F9gag.com')
        print("processing replies :", commentId, end='\r')
        data1 = r1.json()
        replies.extend(data1['payload']['comments'])

    df1 = pd.DataFrame(replies)
    df1['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df1.to_csv(replies1, index=False)
    print("\n" + replies1 + " saved")
    return comments1, replies1

