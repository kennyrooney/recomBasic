import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = dash_app.server
dash_app.config.suppress_callback_exceptions = True


