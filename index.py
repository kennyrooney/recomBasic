import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import check_password, query_password
import apps.content
from app import dash_app
import callbacks




# Simple dash component login form.
login_form = html.Div([
    html.Span("APP Title", className='app-title'),

    html.Div([
        html.P("Please Login below", style={"text-align": "center"}),
        html.Form([
            html.Div(dcc.Input(placeholder='username', name='username'), className='row'),
            html.Div(dcc.Input(placeholder='password', name='password', type='password'), className='row'),
            html.Button('Login', type='submit')
        ], action='/custom-auth/login', method='post')
    ], className='row', style={
                                            "vertical-align": 'center',
                                            "horizontal-align": "center",
                                            "cursor": "pointer",
                                            "marginTop": "0",
                                            "marginBottom": "17",}
        )
    ])


dash_app.layout = html.Div(id='custom-auth-frame')

_app_route = '/dash-core-components/logout_button'
# Create a login route
@dash_app.server.route('/custom-auth/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    queried_password = query_password(username)

    if not username or not password:
        # user name or password not supplied to form
        print("didn't specify user name or password to form")
        flask.abort(401)
    elif queried_password is None:
        # couldn't find user in db
        print("couldn't find user")
        flask.abort(401)
    elif check_password(password.encode(), queried_password) == False:
        # incorrect password
        print("incorrect password")
        flask.abort(401)

    # Return a redirect with
    rep = flask.redirect(_app_route)

    # Here we just store the given username in a cookie.
    # Actual session cookies should be signed or use a JWT token.
    rep.set_cookie('custom-auth-session', username)
    return rep


# create a logout route
@dash_app.server.route('/custom-auth/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect(_app_route)
    rep.set_cookie('custom-auth-session', '', expires=0)
    return rep


@dash_app.callback(Output('custom-auth-frame', 'children'),
              [Input('custom-auth-frame', 'id')])
def dynamic_layout(_):
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return login_form
    return apps.content.layout


if __name__ == '__main__':
    dash_app.run_server(debug=True)

