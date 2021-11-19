import pandas as pd
import json
from datetime import datetime,  timedelta
from dateutil.relativedelta import relativedelta


class Twitter_Prepare:

    def __init__(self, followers, following, tweets):
        self._follower = self.to_pandas(followers)
        self._following = self.to_pandas(following)
        self._tweets = self.to_pandas(tweets)

    def to_pandas(self, dictionary) -> pd.DataFrame:
        return pd.DataFrame(dictionary)

    def follower(self) -> pd.DataFrame:
        return self._follower.copy()

    def following(self) -> pd.DataFrame:
        return self._following.copy()

    def tweets(self) -> pd.DataFrame:
        return self._tweets.copy()

    def follower_count(self):
        return len(self._follower)

    def following_count(self):
        return len(self._following)

    def tweet_count(self):
        return len(self._tweets)

    def like_count(self):
        return self._tweets['like_count'].sum()

    def reply_count(self):
        return self._tweets['reply_count'].sum()

    def retweet_count(self):
        return self._tweets['retweet_count'].sum()

    def quote_count(self):
        return self._tweets['quote_count'].sum()

    def name_url(self, x,y, z):
        return f"{z} [{x}](https://twitter.com/{y})"

    def image_display(self, df):
        df['profile_image_url'] = df['profile_image_url'].apply(lambda x: x.replace('_normal', '_bigger'))
        df['profile_image_url'] = df['profile_image_url'].apply(lambda x: f"![image]({x})")
        return df

    def top10_follower(self):
        df = self.follower()
        df = self.image_display(df)
        df['name'] = df.apply(lambda x: self.name_url(x['name'], x['username'], x['profile_image_url']), axis=1)
        df = df.sort_values(by='followers_count', ascending=False)
        return df.head(10)
    
    def top10_following(self):
        df = self.following()
        df = self.image_display(df)
        df['name'] = df.apply(lambda x: self.name_url(x['name'], x['username'], x['profile_image_url']), axis=1)
        
        df = df.sort_values(by='followers_count', ascending=False)
        return df.head(10)

    def top10_tweets(self):
        df = self.tweets()
        df = self.calc_total_engagement(df)
        df = self.transform_datetime(df, 'created_at')
        df['id'] = df['id'].apply(lambda x: f"[{x}](https://twitter.com/explosion_ai/status/{x})")
        df['created_at'] = df['created_at'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        df = df.sort_values(by='total_engagement', ascending=False)
        return df.head(10)

    def tweets_daily(self, days):
        df = self.tweets()
        df = self.transform_datetime(df, 'created_at')
        df = df.loc[df['created_at'] >= (datetime.today() - relativedelta(days=days))]
        df['created_at'] = df['created_at'].apply(lambda x: x.date())
        df = df.groupby('created_at').agg({'id': 'count', 'reply_count' : 'sum', 'like_count' : 'sum', 'retweet_count' :'sum'}).reset_index()
        df = df.sort_values(by='created_at', ascending=False)
        df = df.rename(columns={"created_at": "date", "id" : "tweet_count"})
        return df


    def tweets_weekly(self, weeks):
        df = self.tweets()
        df = self.transform_datetime(df, 'created_at')
        df = df.loc[df['created_at'] >= (datetime.today() - relativedelta(weeks=weeks))]
        df['created_at'] = df['created_at'].apply(lambda x: x.isocalendar()[1])
        df = df.groupby('created_at').agg({'id': 'count', 'reply_count' : 'sum', 'like_count' : 'sum', 'retweet_count' :'sum'}).reset_index()
        df = df.sort_values(by='created_at', ascending=False)
        df = df.rename(columns={"created_at": "week_number", "id" : "tweet_count"})
        return df

    def tweets_monthly(self, month):
        df = self.tweets()
        df = self.transform_datetime(df, 'created_at')
        df = df.loc[df['created_at'] >= (datetime.today() - relativedelta(month=month))]
        df['created_at'] = df['created_at'].apply(lambda x: x.month)
        df = df.groupby('created_at').agg({'id': 'count', 'reply_count' : 'sum', 'like_count' : 'sum', 'retweet_count' :'sum'}).reset_index()
        df = df.sort_values(by='created_at', ascending=False)
        df = df.rename(columns={"created_at": "month", "id" : "tweet_count"})
        return df

    def calc_total_engagement(self, df):
        df['total_engagement'] = df['reply_count'] + df['like_count'] + df['retweet_count']
        return df

    def transform_datetime(self, df, column):
        df[column] = df[column].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z"))
        return df

    

