from datetime import time
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import Data_Prepare as data_set


app = dash.Dash(__name__)

follower_top10 = px.bar(data_set.get_top10_follower(), x="username", y="followers_count", title="Top 10 Follower")
following_top10 = px.bar(data_set.get_top10_following(), x="username", y="followers_count", title="Top 10 Following")
tweets_top10 = px.bar(data_set.get_top10_tweets(), x="id", y="sum", title="Top 10 Tweet")
recent_tweets = px.bar(data_set.get_top20_recent_tweets(), x="id", y="sum", hover_data=['created_at'], title="Recennt 20 Tweets")
engagement = data_set.get_weekly_engagement()
engagement_daily = data_set.get_daily_engagement()

fig = go.Figure()
fig.add_trace(go.Indicator(
    mode = "number",
    value = len(data_set.follower_main),
    title = {"text" : "Follower"},
    domain = {'row': 0, 'column': 0}
))
fig.add_trace(go.Indicator(
    mode = "number",
    value = len(data_set.following_main),
    title = {"text" : "Following"},
    domain = {'row': 0, 'column': 1}
))
fig.add_trace(go.Indicator(
    mode = "number",
    value = len(data_set.tweets_main),
    title = {"text" : "Tweets"},
    domain = {'row': 0, 'column': 2}
))



fig.add_trace(go.Indicator(
    mode = "number",
    value = sum(list(data_set.tweets_main['like_count'])),
    title = {"text" : "Like Count"},
    domain = {'row': 1, 'column': 0}
))
fig.add_trace(go.Indicator(
    mode = "number",
    value = sum(list(data_set.tweets_main['reply_count'])),
    title = {"text" : "Reply Count"},
    domain = {'row': 1, 'column': 1}
))
fig.add_trace(go.Indicator(
    mode = "number",
    value = sum(list(data_set.tweets_main['retweet_count'])),
    title = {"text" : "Retweet Count"},
    domain = {'row': 1, 'column': 2}
))



fig.update_layout(
    grid = {'rows': 2, 'columns':3, 'pattern': "independent"},
)

data = [
{
    'x' : list(engagement['calender_week']),
    'y' : list(engagement['like_count']),
    'type' : 'lines',
    'name' : 'likes'
},
{
    'x' : list(engagement['calender_week']),
    'y' : list(engagement['reply_count']),
    'type' : 'lines',
    'name' : 'reply'
},
{
    'x' : list(engagement['calender_week']),
    'y' : list(engagement['retweet_count']),
    'type' : 'lines',
    'name' : 'retweet'
},
{
    'x' : list(engagement['calender_week']),
    'y' : list(engagement['id']),
    'type' : 'bar',
    'name' : 'number of tweets'
},
]

data_2 = [
{
    'x' : list(engagement_daily['date']),
    'y' : list(engagement_daily['like_count']),
    'type' : 'lines',
    'name' : 'likes'
},
{
    'x' : list(engagement_daily['date']),
    'y' : list(engagement_daily['reply_count']),
    'type' : 'lines',
    'name' : 'reply'
},
{
    'x' : list(engagement_daily['date']),
    'y' : list(engagement_daily['retweet_count']),
    'type' : 'lines',
    'name' : 'retweet'
},
{
    'x' : list(engagement_daily['date']),
    'y' : list(engagement_daily['id']),
    'type' : 'bar',
    'name' : 'number of tweets'
},
]



app.layout = html.Div(className="Main",children=[
    html.Div(className="Title",children=[
        html.H1('Twitter Reporting')
    ]),
    html.Div(className="KPI",children=[
        html.H2('Monthly'),
        dcc.Graph(
            id='kpis',
            figure=fig,
        ),
    ]),
    html.H2('Engagement'),
    html.Div(className="Engagement",children=[
        dcc.Graph(
        figure={
            'data': data,
            'layout': {
            'title': 'Weekly'
            }
        },
        style={'width': '100%'}),
        dcc.Graph(
        figure={
            'data': data_2,
            'layout': {
            'title': 'Daily'
            }
        },
        style={'width': '100%', 'heigt': '100%'})
    ]),

    html.Div(className="Graphs",children=[
        html.H2('Top Analysis'),
        dcc.Graph(
            id='follower_top10',
            figure=follower_top10,
        ),
        dcc.Graph(
            id='following_top10',
            figure=following_top10
        ),
        dcc.Graph(
            id='tweets_top10',
            figure=tweets_top10
        ),
        dcc.Graph(
            id='recent_tweets',
            figure=recent_tweets
        ),
        

    ])
])



if __name__ == '__main__':
    app.run_server(debug=True)