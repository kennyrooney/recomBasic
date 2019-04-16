from utils import *
from appConfig import jokes_folder
import dash_core_components as dcc


layout = html.Div([

    # header
    html.Div([

        html.Span("APP Title", className='app-title'),
        html.Span(dcc.LogoutButton(logout_url='/custom-auth/logout', style={"background-color": 'black'}),
                  style={"float": "Right"}, className='app-title')


     ], className="row header"),
    html.Div(children=[
    html.Div(id='page-content', className='container', style={"margin": "2% 3%"}),
    html.Div([
        dcc.RadioItems(
            id='rating',
            options=[
                {'label': 'Bad Joke', 'value': '1'},
                {'label': 'Ok Joke', 'value': '2'},
                {'label': 'Average Joke', 'value': '3'},
                {'label': 'Good joke', 'value': '4'},
                {'label': 'Excellent Joke', 'value': '5'},
            ],
            value='3',
            labelStyle={'display': 'inline-block'}
        )

    ], className='container')

    ], className='row'),
    html.Div([
        html.Div(makeJokeOrder(jokes_folder), id='joke-history', style={'display': 'none'}),
        #html.Div('0', id='joke-index', style={'display': 'none'}),
        html.Button('Previous', id='prev-button'),
        html.Button('Next', id='next-button'),
        html.Div(id='test')


               ], id='controls', className='container'),


             ])


