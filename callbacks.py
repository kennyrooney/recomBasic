from dash.dependencies import Input, Output, State
import flask
import os
from app import dash_app
import json
import dash_dangerously_set_inner_html
import dash_html_components as html
from utils import makeJokeOrder, update_rating, create_connection
from appConfig import jokes_folder, sqlite3_db
from flask import Session



@dash_app.callback(Output('page-content', 'children'),
                   [Input('joke-history', 'children')])
def displayJoke(jokes_history):

    if jokes_history is not None:

        jokes_list = json.loads(jokes_history)
        n_jokes = len(jokes_list[0])
        index = jokes_list[1]
        print(index)
        if index == n_jokes:
            return html.P("You have seen all the jokes")

        html_text = '''{}'''.format(open(jokes_list[0][index]).read().replace('\n', ' '))

        return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(html_text)
    else:

        return html.P("Press next to start rating jokes")


@dash_app.callback(Output('joke-history', 'children'),
                   [Input('next-button', 'n_clicks'), Input('prev-button', 'n_clicks')],
                   [State('joke-history', 'children')])
def saveJokesIndex(next_button, previous_button, joke_history):
    print("im saveJokes")

    if joke_history is None:
        return makeJokeOrder(jokes_folder)
    else:
        jokes_list = json.loads(joke_history)
        previous_count = jokes_list[2]
        next_count = jokes_list[3]
    print(next_button, next_count, previous_button, previous_count)
    if next_button is not None and next_button != next_count:
        jokes_list = json.loads(joke_history)
        jokes = jokes_list[0]
        n_jokes = len(jokes)
        jokes_index = jokes_list[1]
        if jokes_index + 1 > n_jokes:
            index = n_jokes
        else:
            index = jokes_index + 1

        return json.dumps([jokes, index, previous_button, next_button])

    elif previous_button is not None and previous_button != previous_count:

        jokes_list = json.loads(joke_history)
        jokes = jokes_list[0]
        jokes_index = jokes_list[1]
        if jokes_index == 0:
            index = 0
        else:
            index = jokes_index - 1

        return json.dumps([jokes, index, previous_button, next_button])

    else:
        return joke_history


@dash_app.callback(Output('test', 'children'), [Input('prev-button', 'n_clicks'), Input('next-button', 'n_clicks')],
          [State('rating', 'value'), State('joke-history', 'children')])
def storeRating(prev_click, next_click, rating, joke_history):
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if rating is not None and joke_history is not None:
        jokes, index, _, _ = json.loads(joke_history)

        joke_number = jokes[index].split(os.sep)[-1].split('init')[1].split('.')[0]
        joke_column = 'joke{}'.format(joke_number)
        j_dict = dict()
        j_dict['joke'] = [joke_column, rating]
        j_dict['user'] = session_cookie
        conn = create_connection(sqlite3_db)
        update_rating(conn, j_dict)
        conn.commit()
        conn.close()

    return None
