from datetime import time
from os import name
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objs as go
from Data_Prepare import Twitter_Prepare
import dash_bootstrap_components as dbc
import json

follower = None
with open('Data/Twitter/EXPLOSION_Follower.json', 'r', encoding='utf8') as f:
    follower = json.load(f)


following = None
with open('Data/Twitter/EXPLOSION_Following.json', 'r', encoding='utf8') as f:
    following = json.load(f)

tweets = None
with open('Data/Twitter/EXPLOSION_Tweets.json', 'r', encoding='utf8') as f:
    tweets = json.load(f)

twitter_object = Twitter_Prepare(follower, following, tweets)
top_10_follower = twitter_object.top10_follower()
top_10_following = twitter_object.top10_following()
top_10_tweets = twitter_object.top10_tweets()

kpi_follower = twitter_object.follower_count()
kpi_following = twitter_object.following_count()
kpi_tweets = twitter_object.tweet_count()
kpi_likes = twitter_object.like_count()
kpi_replies = twitter_object.reply_count()
kpi_retweets = twitter_object.retweet_count()
kpi_quotes = twitter_object.quote_count()

kpis_1 = go.Figure()
kpis_1.add_trace(go.Indicator(
    mode = "number",
    value = kpi_follower,
    title = {"text" : "Follower"},
    domain = {'row': 0, 'column': 0}
))
kpis_1.add_trace(go.Indicator(
    mode = "number",
    value = kpi_following,
    title = {"text" : "Following"},
    domain = {'row': 0, 'column': 1}
))
kpis_1.add_trace(go.Indicator(
    mode = "number",
    value = kpi_tweets,
    title = {"text" : "Tweets"},
    domain = {'row': 0, 'column': 2}
))
kpis_2 = go.Figure()
kpis_2.add_trace(go.Indicator(
    mode = "number",
    value = kpi_likes,
    title = {"text" : "Likes"},
    domain = {'row': 1, 'column': 0}
))
kpis_2.add_trace(go.Indicator(
    mode = "number",
    value = kpi_replies,
    title = {"text" : "Replies"},
    domain = {'row': 1, 'column': 2}
))
kpis_2.add_trace(go.Indicator(
    mode = "number",
    value = kpi_retweets,
    title = {"text" : "Retweets"},
    domain = {'row': 1, 'column': 1}
))
kpis_2.add_trace(go.Indicator(
    mode = "number",
    value = kpi_quotes,
    title = {"text" : "Quotes"},
    domain = {'row': 1, 'column': 3}
))
kpis_1.update_layout(
    grid = {'rows': 1, 'columns':3, 'pattern': "independent"},
)
kpis_2.update_layout(
    grid = {'rows': 1, 'columns':4, 'pattern': "independent"},
)
columns = [
    {"name" : 'name', 'id' : 'name', 'presentation':'markdown'},
    {"name" : 'followers_count', 'id' : 'followers_count'},
    {"name" : 'following_count', 'id' : 'following_count'},
    {"name" : 'tweet_count', 'id' : 'tweet_count'},
    {"name" : "listed_count", "id" : "listed_count"}
]

app = dash.Dash(__name__)
app.layout = html.Div(className="main", children=
[
    html.Div(className="kpi",children=[
        dcc.Graph(
            id='account_kpi',
            figure=kpis_1,
        ),
        dcc.Graph(
            id='tweet_kpi',
            figure=kpis_2,
        ),
    ]),
    html.Div(className="top_tables",children=[
        dash_table.DataTable(
            id='tbl', data=top_10_follower.to_dict('records'),
            columns=columns,
        ),
        html.Br(),
        dash_table.DataTable(
            id='tbl2', data=top_10_following.to_dict('records'),
            columns=columns,
        ),
        html.Br(),
        dash_table.DataTable(
            id='tbl3', data=top_10_tweets.to_dict('records'),
            columns=[{"name": i, "id": i, 'presentation': 'markdown'} for i in top_10_tweets.columns if i not in ['text', 'retweeted_at', 'retweet_id', 'is_retweet', 'total_engagement']],
        ),
    ]),
    html.Div(className="daily",children=[
        
    ]),
    html.Div(className="monthly",children=[
        
    ]),
    html.Div(className="yearly",children=[
        
    ]),
],
)

if __name__ == "__main__":
    app.run_server(debug=True)